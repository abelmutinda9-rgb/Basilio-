from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Attempt to import MovieBox
try:
    from moviebox_api.interactive import MovieBox
except ImportError:
    try:
        from moviebox_api import MovieBox
    except Exception as e:
        print(f"CRITICAL: Could not import moviebox_api: {e}")
        MovieBox = None

app = Flask(__name__)
CORS(app)

# Global engine instance
engine = None

def get_engine():
    global engine
    if engine is not None:
        return engine

    if MovieBox is None:
        print("Error: MovieBox library not loaded.")
        return None

    # List of mirrors - added .ng and .bz which are currently more stable
    default_mirrors = ["www.moviebox.ng", "h5.aoneroom.com", "moviebox.ph", "moviebox.bz"]
    env_mirror = os.getenv("MOVIEBOX_API_HOST")
    mirrors = [env_mirror] + default_mirrors if env_mirror else default_mirrors

    for host in mirrors:
        if not host: continue
        try:
            print(f"Attempting to connect to mirror: {host}")
            # We initialize the engine
            temp_engine = MovieBox(host=host)
            
            # TEST: Try a search to verify the mirror actually responds
            test_search = temp_engine.search_movie("Batman")
            if test_search:
                print(f"SUCCESS: Connected to {host}")
                engine = temp_engine
                return engine
        except Exception as e:
            print(f"FAILED connection to {host}: {str(e)}")
            continue
            
    return None

@app.route('/')
def home():
    e = get_engine()
    return jsonify({
        "status": "active",
        "engine_ready": e is not None,
        "users": 19, # Static or dynamic as per your UI
        "message": "Real MovieBox Engine is Live!" if e else "Engine Warming Up - Checking Mirrors...",
        "active_mirror": getattr(engine, 'host', None) if engine else None
    })

@app.route('/movies')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    e = get_engine()
    if not e:
        return jsonify({"error": "All mirrors are currently unreachable from Render. Try again shortly."}), 503

    try:
        # Perform the actual search
        results = e.search_movie(query)
        
        # Format results for your Lovable/Frontend
        formatted = []
        for m in results:
            formatted.append({
                "id": m.get('id', '0'),
                "title": m.get('title', 'Unknown'),
                "poster": m.get('poster', ''),
                "url": m.get('url', ''), # The streaming source
                "type": m.get('type', 'movie')
            })
        return jsonify(formatted)
    except Exception as err:
        print(f"Search Error: {err}")
        return jsonify({"error": "Search failed", "details": str(err)}), 500

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

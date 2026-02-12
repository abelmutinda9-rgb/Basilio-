from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

# Try to import the library
try:
    from moviebox_api.interactive import MovieBox
except ImportError:
    try:
        from moviebox_api import MovieBox
    except:
        MovieBox = None

app = Flask(__name__)
CORS(app)

# Global variable for the engine
engine = None

def get_engine():
    global engine
    if engine is None and MovieBox is not None:
        # List of mirrors to try
        mirrors = [os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com"), "moviebox.ph", "moviebox.ke"]
        for host in mirrors:
            try:
                print(f"Trying to wake up mirror: {host}")
                engine = MovieBox(host=host)
                # Quick test
                engine.search_movie("Avengers")
                print(f"Success! Connected to {host}")
                return engine
            except:
                engine = None
                continue
    return engine

@app.route('/')
def home():
    e = get_engine()
    return {
        "status": "active",
        "engine_ready": e is not None,
        "users": 19,
        "message": "Real MovieBox Engine is Live!" if e else "Engine Warming Up..."
    }

@app.route('/movies')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    e = get_engine()
    if not e:
        return jsonify({"error": "Mirrors are busy. Try again in 10 seconds."}), 503

    try:
        # REAL MovieBox Search
        results = e.search_movie(query)
        
        # Format the data for Lovable
        formatted = []
        for m in results:
            formatted.append({
                "id": m.get('id', '0'),
                "title": m.get('title', 'Unknown'),
                "poster": m.get('poster', ''),
                "url": m.get('url', '') # This is the REAL streaming link
            })
        return jsonify(formatted)
    except Exception as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

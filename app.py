from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# --- 1. SMART IMPORT ---
try:
    from moviebox_api.interactive import MovieBox
except ImportError:
    try:
        from moviebox_api import MovieBox
    except ImportError:
        MovieBox = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 2. ENGINE INITIALIZATION WITH FAILOVER ---
engine = None
primary_host = os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com")
backup_host = "moviebox.ke"

if MovieBox:
    try:
        # Try Primary
        engine = MovieBox(host=primary_host)
        print(f"Engine loaded on {primary_host}")
    except Exception as e:
        print(f"Primary failed: {e}. Trying backup...")
        try:
            # Try Backup
            engine = MovieBox(host=backup_host)
            print(f"Engine loaded on {backup_host}")
        except Exception as e2:
            print(f"All mirrors failed: {e2}")
            engine = None
else:
    print("MovieBox library not found in environment.")

# --- 3. ROUTES ---
@app.route('/')
def home():
    return {
        "status": "active",
        "message": "Movie Engine is Live!",
        "engine_loaded": engine is not None,
        "mirror": primary_host if engine else "none"
    }

@app.route('/movies')
def search():
    query = request.args.get('q', '')
    if not engine:
        return jsonify({"error": "Engine not loaded. Check mirror hosts."}), 500
    
    if not query:
        return jsonify([])

    try:
        # Search real movies
        results = engine.search_movie(query)
        
        # Format for Lovable
        formatted = []
        for movie in results:
            formatted.append({
                "id": movie.get('id', ''),
                "title": movie.get('title', 'Unknown'),
                "poster": movie.get('poster', ''),
                "url": movie.get('url', '')
            })
        return jsonify(formatted)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

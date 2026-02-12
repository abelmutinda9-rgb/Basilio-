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
# Universal CORS to ensure Lovable never gets blocked
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 2. ENGINE INITIALIZATION WITH AUTO-RETRY ---
engine = None
# We try these three in order. One of them WILL work.
mirrors = [
    os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com"),
    "moviebox.ph",
    "moviebox.ke"
]

active_mirror = "none"

if MovieBox:
    for host in mirrors:
        try:
            print(f"Attempting to load engine on: {host}")
            temp_engine = MovieBox(host=host)
            # We do a 'test' search to make sure the mirror is actually alive
            test_search = temp_engine.search_movie("Avengers")
            if test_search is not None:
                engine = temp_engine
                active_mirror = host
                print(f"SUCCESS: Engine live on {host}")
                break
        except Exception as e:
            print(f"FAILED on {host}: {e}")
            continue
else:
    print("CRITICAL: moviebox-api library not installed.")

# --- 3. ROUTES ---
@app.route('/')
def home():
    return {
        "status": "active",
        "message": "Movie Engine is Live!",
        "engine_loaded": engine is not None,
        "mirror": active_mirror,
        "users_limit": 19
    }

@app.route('/movies')
def search():
    query = request.args.get('q', '')
    if not engine:
        return jsonify({"error": "Engine not loaded. All mirrors failed."}), 500
    
    if not query:
        # If no search, return a default list so the app isn't empty
        query = "Avengers"

    try:
        results = engine.search_movie(query)
        
        # Format for Lovable's UI
        formatted = []
        for movie in results:
            formatted.append({
                "id": movie.get('id', '0'),
                "title": movie.get('title', 'Unknown'),
                "poster": movie.get('poster', ''),
                "url": movie.get('url', '') # Direct stream link
            })
        return jsonify(formatted)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render default port is 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
                                     

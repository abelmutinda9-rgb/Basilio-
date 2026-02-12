from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# --- SMART IMPORT LOGIC ---
# This ensures the app finds the MovieBox engine regardless of the version
try:
    from moviebox_api.interactive import MovieBox
except ImportError:
    try:
        from moviebox_api.main import MovieBox
    except ImportError:
        try:
            import moviebox_api
            MovieBox = moviebox_api.MovieBox
        except Exception as e:
            print(f"Critical Import Error: {e}")
            MovieBox = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Engine
# Using the host you set in Render (defaulting to h5.aoneroom.com)
try:
    engine = MovieBox(host=os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com")) if MovieBox else None
except Exception as e:
    print(f"Engine Init Error: {e}")
    engine = None

@app.route('/')
def home():
    return {
        "status": "active",
        "message": "Movie Engine is Live!",
        "engine_loaded": engine is not None
    }

@app.route('/movies')
def search():
    query = request.args.get('q', 'Avengers')
    
    if not engine:
        return jsonify({"error": "Movie engine not initialized. Check logs."}), 500

    try:
        # Search real movies using the Simatwa engine
        results = engine.search_movie(query)
        
        # Format the data for Lovable
        formatted_results = []
        for movie in results:
            formatted_results.append({
                "id": movie.get('id', ''),
                "title": movie.get('title', 'Unknown Title'),
                "poster": movie.get('poster', ''),
                "url": movie.get('url', '') # This is for the inbuilt player
            })
        return jsonify(formatted_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

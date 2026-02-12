from flask import Flask, request, jsonify
from flask_cors import CORS
from moviebox_api.interactive import MovieBox
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Real Engine
engine = MovieBox(host=os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com"))

@app.route('/')
def home():
    return "Movie Engine is Live!"

@app.route('/movies')
def search():
    query = request.args.get('q', 'Avengers')
    try:
        # Search real movies
        results = engine.search_movie(query)
        # Transform the data so Lovable understands it
        formatted_results = []
        for movie in results:
            formatted_results.append({
                "id": movie.get('id'),
                "title": movie.get('title'),
                "poster": movie.get('poster'),
                "url": movie.get('url') # For the player
            })
        return jsonify(formatted_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

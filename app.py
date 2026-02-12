from flask import Flask, request, jsonify
from flask_cors import CORS
from moviebox_api.interactive import MovieBox
import os

app = Flask(__name__)
CORS(app) # This allows Lovable to talk to Render

# Start the MovieBox engine
# Using the host you set in Render variables
engine = MovieBox(host=os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com"))

@app.route('/')
def home():
    return {"status": "active", "message": "Movie Engine is Ready"}

@app.route('/movies')
def search_movies():
    query = request.args.get('q', 'Avengers') # Default to Avengers if no search
    try:
        # This calls the Simatwa engine to find movies
        results = engine.search_movie(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
  

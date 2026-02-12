from flask import Flask, request, jsonify
from flask_cors import CORS
from moviebox_api.interactive import MovieBox
import os

app = Flask(__name__)
CORS(app)

# Connect to the MovieBox engine
engine = MovieBox(host=os.getenv("MOVIEBOX_API_HOST", "h5.aoneroom.com"))

@app.route('/')
def home():
    return "Movie Engine is Live!"

# THIS IS THE PART LOVABLE IS LOOKING FOR:
@app.route('/movies')
def search():
    query = request.args.get('q', 'Avengers')
    try:
        results = engine.search_movie(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

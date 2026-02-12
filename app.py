from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
# This tells Render to let ANYONE (especially Lovable) see the data
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Movie Engine is Live!"

@app.route('/movies')
def search():
    query = request.args.get('q', 'Avengers')
    # Returning a list of movies directly so Lovable doesn't get confused
    return jsonify([
        {"title": "Avengers: Endgame", "id": "1", "poster": "https://via.placeholder.com"},
        {"title": "Avengers: Infinity War", "id": "2", "poster": "https://via.placeholder.com"}
    ])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
  

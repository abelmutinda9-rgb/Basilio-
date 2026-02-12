from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Movie Engine is Live!"

@app.route('/movies')
def search():
    query = request.args.get('q', 'Avengers')
    # This is a test response to make sure Lovable can connect
    return jsonify({"status": "connected", "query": query, "message": "Backend is talking to Lovable!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
  

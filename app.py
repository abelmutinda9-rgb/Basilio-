from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from moviebox_api.interactive import MovieBox # Standard import for Simatwa's API

app = Flask(__name__)
CORS(app)

# This is the "Engine" the app was looking for
def get_engine():
    try:
        # We try a stable mirror like .ng or .ph
        host = os.getenv("MOVIEBOX_API_HOST", "www.moviebox.ng")
        engine = MovieBox(host=host)
        return engine
    except Exception as e:
        print(f"Engine failed to start: {e}")
        return None

@app.route('/')
def home():
    engine = get_engine()
    return jsonify({
        "status": "active",
        "engine_ready": engine is not None,
        "message": "Engine is Live!" if engine else "Engine Warming Up..."
    })

@app.route('/movies')
def search():
    query = request.args.get('q', '')
    engine = get_engine()
    if not engine or not query:
        return jsonify([])
    
    # Simatwa's search method
    results = engine.search_movie(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
    

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"status": "API is Live", "source": "vidsrc"})

@app.route('/get-source')
def get_source():
    movie_id = request.args.get('id') # Expecting an IMDB ID like 'tt1234567'
    
    if not movie_id:
        return jsonify({"error": "No ID provided"}), 400

    # The actual URL format for vidsrc.me
    # Note: Using /embed/ enables the player logic
    direct_link = f"https://vidsrc.me{movie_id}" 
    
    return jsonify({
        "video_url": direct_link,
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://vidsrc.me"
        }
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    

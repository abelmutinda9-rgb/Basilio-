import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get-source')
def get_source():
    movie_id = request.args.get('id')
    # We use a 'Public Resolver' that is known for being ad-free/low-ad
    # This returns a JSON object with the direct .m3u8 or .mp4 link
    direct_link = f"https://vidsrc.me{movie_id}" 
    
    return jsonify({
        "video_url": direct_link,
        "headers": {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://vidsrc.me"
        }
    })
    

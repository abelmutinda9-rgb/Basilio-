import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# Try all known ways to import the MovieBox class
try:
    from moviebox_api.interactive import MovieBox
except (ImportError, ModuleNotFoundError):
    try:
        from moviebox_api import MovieBox
    except (ImportError, ModuleNotFoundError):
        try:
            from moviebox_api.moviebox import MovieBox
        except:
            MovieBox = None
            print("CRITICAL: MovieBox class not found in any known module path.")
            

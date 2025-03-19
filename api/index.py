# import flask
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import time
from urllib.parse import urlparse
import requests  # Add this import

# Initialize Flask app
app = Flask(__name__)

# Get Blender path from environment variable (will need to be configured in Vercel)
BLENDER_EXEC = os.getenv('BLENDER_EXEC', "/Applications/Blender.app/Contents/MacOS/Blender")
UPLOAD_FOLDER = '/tmp'  # Use /tmp for serverless functions

@app.route('/api', methods=['GET'])
def home():
    return jsonify({'status': 'ok', 'message': 'API is running'})

# create the route that handles the file logic
@app.route('/api/process_model', methods=['POST'])
def process_model():
    try:
        data = request.json
        
        # Download the file from the URL
        if file_path := data.get("file_path"):
            local_file = download_from_url(file_path)
            return jsonify({"status": "success", "local_file": local_file})
        else:
            return jsonify({"error": "No input URL provided"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def download_from_url(url):
    """Download a file from URL to local storage"""
    local_filename = os.path.join(UPLOAD_FOLDER, secure_filename(f"model_{int(time.time())}.obj"))
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload directory exists
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except requests.exceptions.RequestException as e:
# sourcery skip: raise-specific-error
        raise Exception(f"Failed to download file: {str(e)}") from e
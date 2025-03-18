# import flask
from flask import Flask, request, jsonify

# create an app instance
app = Flask(__name__)

# Get Blender path from Homebrew
BLENDER_EXEC = "/Applications/Blender.app/Contents/MacOS/Blender"

@app.route('/')
def home():
    return 'Hello, World!'

# create the route that handles the file logic
@app.route('/process_model', methods=['POST'])
def process_model():
    file_path = request.json.get("file_path")

    print(file_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
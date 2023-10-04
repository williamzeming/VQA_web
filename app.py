import os

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="webroot")
CORS(app)

@app.route('/')
# @app.route('/<path:path>')
def index():
    return send_from_directory(app.static_folder, 'index.html')


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "file": filepath}), 200

    return jsonify({"error": "Invalid file type"}), 400


@app.route('/get_filelist', methods=['GET'])
def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)


@app.route('/get_filepath', methods=['POST'])
def get_filepath():
    filename = request.json.get('filename')
    filepath = filename
    print(filepath)
    return jsonify(filepath=filepath)


@app.route('/pdfs/<filename>', methods=['GET'])
def serve_pdf(filename):
    return send_from_directory(directory='uploads', path=filename)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8988, debug=True)

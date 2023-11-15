import os
import random
from annotation.preprocess.preprocess import preprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
# from flask_uploads import UploadSet, configure_uploads, DOCUMENTS, patch_request_class
from flask_cors import CORS
from werkzeug.utils import secure_filename
from chatbot import ChatBot

app = Flask(__name__, static_folder="webroot")
CORS(app)
cbot = ChatBot()


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


def loadtxt(file_name):
    folder_path = './annotation/demoTXT'
    base_name, ext = os.path.splitext(file_name)
    new_filename = base_name + ".txt"
    full_path = os.path.join(folder_path, new_filename)
    with open(full_path, 'r', encoding='utf-8') as file:
        testPDF = file.read()
    return testPDF


@app.route('/pdfs/<filename>', methods=['GET'])
def serve_pdf(filename):
    txt = loadtxt(filename)
    cbot.send_initial_message(txt)
    return send_from_directory(directory='uploads', path=filename)


@app.route('/images/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(directory='annotation/visualized', path=filename, as_attachment=True)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    print(message)
    reply = cbot.chat(message + "Don't give me the source yet")
    source = cbot.chat(
        "find the last answer's source. Enclose all your work for this step within triple quotes (\"\"\")., strictly write as format \'Sources: [Page number: page_no, Section: sectionName]\' , do not write another things in this question!")
    response = {
        'reply': reply,
        'source': source
    }
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run('127.0.0.1', port=8988, debug=True)

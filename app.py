from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import gzip
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/converted'
ALLOWED_EXTENSIONS = {'gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_gz_to_csv(filepath, output_folder):
    filename = os.path.basename(filepath).replace('.gz', '.csv')
    output_path = os.path.join(output_folder, filename)
    
    with gzip.open(filepath, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return output_path

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')
        converted_files = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)

                converted_file = convert_gz_to_csv(file_path, app.config['OUTPUT_FOLDER'])
                converted_files.append(converted_file)

        return render_template("index.html", success=True, files=converted_files)

    return render_template("index.html", success=False)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

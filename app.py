from flask import Flask, render_template, request, send_from_directory
import os
import gzip
import shutil

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_gz_to_csv(input_path, output_path):
    """ Convert .csv.gz to .csv """
    try:
        with gzip.open(input_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    for file in files:
        if file.filename.endswith('.csv.gz'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            output_file = file.filename.replace('.gz', '')
            convert_gz_to_csv(filepath, os.path.join(OUTPUT_FOLDER, output_file))
    return "Conversion Successful!"

if __name__ == '__main__':
    app.run(debug=True)

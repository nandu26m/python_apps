import os
import gzip
import shutil
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "converted"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    if not file.filename.endswith(".csv.gz"):
        return "Invalid file type. Please upload a .csv.gz file.", 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, file.filename.replace(".gz", ""))

    # Save uploaded file
    file.save(input_path)

    # Convert .csv.gz to .csv
    try:
        with gzip.open(input_path, "rb") as f_in:
            with open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        return f"Conversion failed: {str(e)}", 500

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

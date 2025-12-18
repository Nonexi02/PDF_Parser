import os
from flask import Flask, render_template, request
import pdfplumber

# Flask app
app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber"""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


@app.route("/", methods=["GET", "POST"])
def index():
    extracted_text = None

    if request.method == "POST":
        file = request.files.get("pdf")

        if file and file.filename.endswith(".pdf"):
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            extracted_text = extract_text_from_pdf(file_path)

    return render_template("index.html", result=extracted_text)


if __name__ == "__main__":
    app.run(debug=True)

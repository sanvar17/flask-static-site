from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta a Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/4.00/'

@app.route('/')
def upload_file():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        txt_path = file_path.rsplit('.', 1)[0] + '.txt'
        convert_pdf_to_text(file_path, txt_path)
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=txt_path, as_attachment=True)

def convert_pdf_to_text(pdf_path, txt_path):
    images = convert_from_path(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        for image in images:
            text = pytesseract.image_to_string(image, lang='spa')
            txt_file.write(text + "\n")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

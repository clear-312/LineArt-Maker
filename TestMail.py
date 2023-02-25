import os
from flask import Flask, request, send_from_directory,render_template
import cv2
from pathlib import Path

app = Flask(__name__,template_folder="template")
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['DOWNLOAD_FOLDER'] = Path('downloads')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Get uploaded image
    image = request.files['image']

    # Save uploaded image to uploads folder
    image.save((app.config['UPLOAD_FOLDER'] / image.filename).resolve())

    # Load uploaded image
    img = cv2.imread((app.config['UPLOAD_FOLDER'] / image.filename).resolve().as_posix())

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply median blur filter to remove noise
    gray = cv2.medianBlur(gray, 5)

    # Apply Canny edge detection to generate the line art
    edges = cv2.Canny(gray, 50, 150)

    # Save the line art to downloads folder
    cv2.imwrite((app.config['DOWNLOAD_FOLDER'] / 'line_art.jpg').resolve().as_posix(), edges)

    # Return the line art as a file download
    return send_from_directory(app.config['DOWNLOAD_FOLDER'].resolve().as_posix(), 'line_art.jpg', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')

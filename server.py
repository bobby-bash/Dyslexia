from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import base64
import re

import easyocr

app = Flask(__name__)
CORS(app)
read = easyocr.Reader(['en'])

@app.route('/')
def hello():
  return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    data = request.get_json()
    image_data = data['image']
    
    # Remove the data:image/png;base64, part
    image_data = re.sub('^data:image/.+;base64,', '', image_data)
    image_data = base64.b64decode(image_data)
    
    # Save the image to a file
    with open('handwriting.png', 'wb') as f:
        f.write(image_data)

    image_path = 'handwriting.png'

    text = read.readtext(image_path, detail=0) 

    print("Extracted Text:")
    print(text)

    return jsonify({'message': 'Image saved successfully!', 'text': text}), 200

if __name__ == '__main__':
    app.run(debug=True)


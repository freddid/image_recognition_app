from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

# Загрузка модели
model = load_model('model/image_recognition_model.h5')

# Классы CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files and 'imageData' not in request.form:
        return redirect(request.url)

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join('static/uploads', file.filename)
            file.save(file_path)
            return redirect(url_for('predict', file_path=file_path))

    if 'imageData' in request.form:
        image_data = request.form['imageData']
        image_data = image_data.split(',')[1]
        image_data = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_data)).convert('RGB')
        file_path = os.path.join('static/uploads', 'captured_image.png')
        image.save(file_path)
        return redirect(url_for('predict', file_path=file_path))

@app.route('/predict')
def predict():
    file_path = request.args.get('file_path')
    img = image.load_img(file_path, target_size=(32, 32))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    return render_template('result.html', file_path=file_path, predicted_class=predicted_class)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

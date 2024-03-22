from flask import Flask, request 
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf  

app = Flask(__name__)
model = tf.keras.models.load_model('final_model.h5') # Load your model
model.summary()

@app.route('/test', methods=['GET'])
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    # Saving file to current directory
    file.save(os.path.join("./", filename))
    # Process the image and compute result string here
    result_str = "your processing result"
    return result_str

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file'] # Get the image from the request
    filename = secure_filename(file.filename)
    file.save(filename) # Save the image
    
    # Load and preprocess the image
    image_size = (224, 224) # Use your model's expected input size
    im = tf.keras.utils.load_img(filename, target_size=image_size)
    # im = tf.keras.utils.load_img(filename, target_size=image_size, keep_aspect_ratio=True)
    # im = tf.keras.utils.load_img(filename, target_size=image_size, interpolation='nearest')
    im = tf.keras.utils.img_to_array(im)
    im = np.expand_dims(im, axis=0) # Expand dims to add batch size of 1
    # im /= 255.0 # Normalize image (if needed according to your model)

    # Use the model to make a prediction
    preds = model.predict(im)
    pred_class = 'positive' if preds[0] >= 0.5 else 'negative'

    print(f'prediction = {preds}')
    # Return the prediction
    return str(pred_class) # change it to 'return str(preds)' if your task is binary instead of multiclass


if __name__ == '__main__':
    app.run(debug=True, port=8000) 
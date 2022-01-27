import flask
from flask import Flask, render_template, request

import os
from tensorflow.keras.preprocessing.image import  load_img, img_to_array
from keras.models import load_model 
import numpy as np
import class_names

app = Flask(__name__)

prediction_names = class_names.CLASS_NAMES
image_folder = os.path.join('static', 'images')
app.config["UPLOAD_FOLDER"] = image_folder

model = load_model('saved_model/')

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    # predicting images
    imagefile = request.files['imagefile']
    image_path = './static/images/' + imagefile.filename 
    imagefile.save(image_path)

    # img = image.load_img(image_path, target_size=(300, 300))
    # x = image.img_to_array(img)
    # x = np.expand_dims(x, axis=0)

    # images = np.vstack([x])
    # classes = model.predict(images, batch_size=10)

    # load an image from file
    image = load_img(image_path, target_size=(256, 256))
    image_array = img_to_array(image)

    # reshape data for the model
    image_array = image_array.reshape((1, image_array.shape[0], image_array.shape[1], image_array.shape[2]))

    # predict the probability across all output classes
    yhat = model.predict(image_array)[0]


    pic = os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename)

    best_guess = prediction_names[np.argmax(yhat)] +" "+ str(yhat[np.argmax(yhat)])
    
    return render_template('index.html', user_image=pic, prediction_text=best_guess)
 

if __name__=='__main__':
  app.run(debug=True, port=5000)
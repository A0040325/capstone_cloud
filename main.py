# Required imports
import base64
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import requests
from PIL import Image
import time
import logging

import io
import numpy as np
import cv2
from keras.models import Model, load_model
from pyfcm import FCMNotification

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate("b21-cap0153adhiganawasa-firebase-adminsdk-4nb1s-85265cd2ca.json")
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('data')
# Initialize FCM
push_service = FCMNotification(api_key="AAAAilZGMnE:APA91bEwgyJklm8jz8v1qxwllnK7sDb6-ETiN-4esdwg5u-C6FVbx2dk5a9TTt9eZTYEyPm4TtxGEjDu357sHZ8jb5tjAGKgB_HwzrcfZzxbfLkHnwzWq3e29WJGkBitVuD6hQfcS8o2")
model1 = load_model('my_modelwithl2.h5')

try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=True
  )
except ImportError:
  pass

@app.route("/", methods=["GET"])
def hello():
    """ Return a friendly HTTP greeting. """
    #todo = todo_ref.document("wrGedrVu6IXHIx5IGzsy").get()
    
    return "Hello World! Welcome To Violence Detection Server, Auth: Hafizh F\n"
    #return jsonify(todo.to_dict()), 200

@app.route('/predict', methods=['POST'])
def predict():
    to_predict = []
    X_tr = []
    usedImages = []

    num_frames = 16
    img_rows,img_cols=128, 128

    classes ='System Start, Collecting Frames'

    payload = request.form.to_dict(flat=False)
    im_b64 = payload['image']

    for i in range(len(im_b64)):
        im_binary = base64.b64decode(im_b64[i])
        buf = io.BytesIO(im_binary)
        img = Image.open(buf)
        to_predict.append(np.array(img))

    if len(to_predict) == num_frames:
        for frameData in to_predict:
            frame1 = cv2.cvtColor(frameData, cv2.COLOR_BGR2RGB)
            frame1 = cv2.resize(frame1, (img_rows,img_cols), interpolation=cv2.INTER_AREA)
            gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            usedImages.append(gray)

        input_img = np.array(usedImages)
        ipt=np.rollaxis(np.rollaxis(input_img,2,0),2,0)
        ipt=np.rollaxis(ipt,2,0)
        X_tr.append(ipt)
        X_tr_array = np.array(X_tr)
        test_pred =model1.predict(X_tr_array)
        result = np.argmax(test_pred, axis =1)
        print(test_pred)
        if result[0] == 0:
            classes = 'Non Violence'
        else:
            classes = 'Violence'
            todo_ref.add({'address': 'TEST',
            'camera_name': 'dulgimo',
            'coordinate': firestore.GeoPoint(-7.285113, 112.796504),
            'created_at': time.time(),
            'photo': im_b64[8],
            'resolved': False,
            'resolved_by': '',
            'updated_at': None,
            'user': 'Joni',
            'phone': '087899998888'
            })


            result = push_service.notify_topic_subscribers(
            message_title="Jaga Bersama",
            topic_name="violence",
            message_body="Kasus Kekerasan Baru Terdeteksi")
        
    return jsonify({'msg': 'success', 'classes': classes}), 200


if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="localhost", port=8080, debug=True)
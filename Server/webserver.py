from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os
import json
import cv2
import io
import argparse
import six
import numpy as np
import time
from PIL import Image

app = Flask(__name__)

@app.route("/objectdetection/", methods=['POST'])
def detection():
    net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]  
        
    photos = request.files["image"]
    detection=photos.read()
    imageinput = six.BytesIO()
    imageinput.write(detection)
    imageinput.seek(0)
    src = Image.open(imageinput)
    process = cv2.cvtColor(np.asarray(src), cv2.COLOR_RGB2BGR)   

      
   
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1]
                     for i in net.getUnconnectedOutLayers()]
    img = cv2.resize(process, None, fx=0.4, fy=0.4)
    blob = cv2.dnn.blobFromImage(
        process, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)
    detected_objects = []
    dictionary = {"objects": detected_objects}

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0:
                detected_objects.append(
                    {"label": str(classes[class_id]), "accuracy": str(round(confidence * 100, 2))})

    return jsonify(dictionary)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000,threaded=True)
    
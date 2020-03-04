# How to read a file into GCP Cloud Functions

import os
from flask import render_template, flash, redirect, request
import cv2
from flask import Flask
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def stitch():
    #read image file string data
    filestr = request.files['file'].read()
    #convert string data to numpy array
    npimg = np.fromstring(filestr, np.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR) 
    return f'{img.shape}'
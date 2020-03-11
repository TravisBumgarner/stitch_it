import os
import uuid

from flask import Flask, render_template, flash, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from google.cloud import storage
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import imutils
from skimage import io 
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')


def kmeans_image(img):
    pixels = np.float32(img.reshape(-1, 3))

    n_colors = 3
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)

    return np.uint8(palette[-1])


def stitch_image(filestr, horizontal_samples_user_input, stitch_style, stitch_size, stitch_spacing):
    npimg = np.frombuffer(filestr, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
    
    img = imutils.resize(img, width=1000)
    img = imutils.resize(img, height=1000) # imutils will not respect both width and height at same time
    input_width, input_height, *_ = img.shape

    if len(img.shape) > 2 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    sample_size = round(input_width / horizontal_samples_user_input)
    vertical_samples = round(input_height / sample_size)

    output_html = ''

    output_html += '\t\t<div id="wrapper"><div id="image">\n'
    
    for i in range(0, horizontal_samples_user_input):
        output_html += '\t\t\t<div class="row">\n'
        
        for j in range(0, vertical_samples):
            i_start = i*sample_size
            i_end = i*sample_size+sample_size
            j_start = j*sample_size
            j_end = j*sample_size+sample_size

            b,g,r = kmeans_image(img[i_start:i_end, j_start:j_end])
            output_html += f'\t\t\t\t<div style="background-color: rgb({r},{g},{b});" class="cell"></div>\n'
        
        output_html += '\t\t\t</div>\n'
    
    output_html += '\t\t</div></div>\n'
    return output_html


# def save_to_bucket(html_body):
#     client = storage.Client()
#     bucket = client.get_bucket("test_stitching")
#     blob = storage.Blob(f'{uuid.uuid4().hex}.html', bucket)
#     blob.upload_from_string(html_body, "text/html")


class StitchForm(FlaskForm):
    horizontal_samples_user_input = IntegerField(
        'Stitch Count Along Vertical Side',
        default=100,
        validators=[
            DataRequired('Stitch Count Along Vertical Side is required'),
            NumberRange(1, 1000, "A vertical stitch count between 1 and 1000 is required")
        ]
    )
    stitch_size = IntegerField(
        'Stitch Diameter',
        default=10,
        validators=[
            DataRequired('The field stitch size is required'),
            NumberRange(1, 1000, "A stitch size between 1 and 1000 is required")
        ]
    )
    stitch_style = RadioField(
        'Stitch Style',
        choices=[
            (0,'Square'),
            (25,'Rounded Square'),
            (50,'Circle')
        ],
        default=25,
        coerce=int,
        validators=[
            DataRequired(),
            NumberRange(0, 50, "A stitch style between 0 and 50 is required")
        ]
    )
    stitch_spacing = IntegerField(
        'Spacing Between Stitches',
        default=0,
        validators=[
            # Cannot validate = 0, because of some bug in wtforms.
            NumberRange(-1000, 1000, "A stitch style between -1000 and 1000 is required")
        ]
    )
    photo = FileField(
        'Photo',
        validators=[
            DataRequired("A photo is required")
        ]
    )
    submit = SubmitField(
        'Stitch!'
    )


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/health-check', methods=['GET'])
def health_check():
    return "ok"

@app.route('/', methods=['GET', 'POST'])
def stitch(): #This function should be split out so it's callable from flask and GCP
    form = StitchForm()

    if form.validate_on_submit():
        stitched_image = stitch_image(
            filestr=request.files[form.photo.name].read(),
            horizontal_samples_user_input=form.horizontal_samples_user_input.data,
            stitch_size=form.stitch_size.data,
            stitch_style=form.stitch_style.data,
            stitch_spacing=form.stitch_spacing.data
        )

        rendered_template = render_template(
            "results.html",
            results = stitched_image,
            stitch_size=form.stitch_size.data,
            stitch_style=form.stitch_style.data,
            stitch_spacing=form.stitch_spacing.data
        ) 
        # try:
        #     save_to_bucket(rendered_template)
        # except:
        #     pass

        return rendered_template
    if (form.errors):
        flash(form.errors)
    return render_template('form.html', title='Stitch', form=form)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

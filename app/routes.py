import os
from app import app
from flask import render_template, flash, redirect, request as flask_request
from app.forms import StitchForm
from app.stitch import stitch_image
from app.gcp_utilities import save_to_bucket
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def stitch(gcp_request=None): #This function should be split out so it's callable from flask and GCP
    request = gcp_request if gcp_request else flask_request # this line is gross?
    form = StitchForm(meta={'csrf': False})
    if form.is_submitted():
        print(form.photo.data)
    if form.validate_on_submit():
        print(request.files)

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
        save_to_bucket(rendered_template)

        return rendered_template
    if (form.errors):
        flash(form.errors)
    return render_template('form.html', title='Stitch', form=form)

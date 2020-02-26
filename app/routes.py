import os
from app import app
from flask import render_template, flash, redirect, request
from app.forms import StitchForm
from app.stitch import stitch_image

@app.route('/', methods=['GET', 'POST'])
def stitch():
    form = StitchForm()
    return render_template('stitch.html', title='Stitch', form=form)


@app.route('/success', methods = ['POST'])  
def success():
    form = StitchForm()

    stitched_image = stitch_image(
        image=form.photo.data,
        horizontal_samples_user_input=form.horizontal_samples_user_input.data,
        stitch_size=form.stitch_size.data,
        stitch_style=form.stitch_style.data,
        stitch_spacing=form.stitch_spacing.data
    )

    return render_template(
        "success.html",
        results = stitched_image,
        stitch_size=form.stitch_size.data,
        stitch_style=form.stitch_style.data,
        stitch_spacing=form.stitch_spacing.data
    ) 
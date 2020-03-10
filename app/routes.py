import os
from app import app
from flask import render_template, flash, redirect, request
from app.forms import StitchForm
from app.stitch import stitch_image

@app.route('/', methods=['GET', 'POST'])
def stitch():
    form = StitchForm(request.form)
    if form.validate_on_submit():
        stitched_image = stitch_image(
            image=form.photo.data,
            horizontal_samples_user_input=form.horizontal_samples_user_input.data,
            stitch_size=form.stitch_size.data,
            stitch_style=form.stitch_style.data,
            stitch_spacing=form.stitch_spacing.data
        )

        return render_template(
            "results.html",
            results = stitched_image,
            stitch_size=form.stitch_size.data,
            stitch_style=form.stitch_style.data,
            stitch_spacing=form.stitch_spacing.data
        ) 
    if (form.errors):
        flash(form.errors)
    return render_template('form.html', title='Stitch', form=form)

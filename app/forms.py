from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, RadioField
from wtforms.validators import DataRequired


class StitchForm(FlaskForm):
    horizontal_samples_user_input = IntegerField('Vertical Stitch Count', default=25)
    stitch_size = IntegerField('Stitch Size', default=10)
    stitch_style = RadioField('Stitch Style', choices=[
        (0,'Square'),
        (25,'Rounded Square'),
        (50,'Circle')
    ])
    stitch_spacing = IntegerField('Stitch Spacing', default=2)
    photo = FileField('Photo', validators=[DataRequired()])
    submit = SubmitField('Stitch!')
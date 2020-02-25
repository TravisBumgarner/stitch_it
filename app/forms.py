from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, RadioField
from wtforms.validators import DataRequired


class StitchForm(FlaskForm):
    sample_size = IntegerField('Sample Size')
    stitch_size = IntegerField('Stitch Size')
    stitch_style = RadioField('Stitch Style', choices=[
        (0,'Square'),
        (25,'Rounded Square'),
        (50,'Circle')
    ])
    stitch_spacing = IntegerField('Stitch Spacing')
    photo = FileField('Photo', validators=[DataRequired()])
    submit = SubmitField('Stitch!')
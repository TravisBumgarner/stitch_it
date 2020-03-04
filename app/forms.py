from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange


class StitchForm(FlaskForm):
    horizontal_samples_user_input = IntegerField(
        'Vertical Stitch Count',
        default=25,
        validators=[
            DataRequired('The field vertical stitch count is required'),
            NumberRange(1, 1000, "A vertical stitch count between 1 and 1000 is required")
        ]
    )
    stitch_size = IntegerField(
        'Stitch Size',
        default=10,
        validators=[
            DataRequired('The field stitch size is required')
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
        'Stitch Spacing',
        default=2,
        validators=[
            DataRequired('The field stitch spacing is required')
        ]
    )
    photo = FileField(
        'Photo',
        validators=[
            DataRequired('The field photo is required')
        ]
    )
    submit = SubmitField(
        'Stitch!'
    )
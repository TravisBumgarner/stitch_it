from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class StitchForm(FlaskForm):
    stitch_size = IntegerField('Stitch Size')
    sample_size = IntegerField('Sample Size')
    stitch_radius = IntegerField('Border Radius')
    stitch_padding = IntegerField('Border Radius')
    photo = FileField('Photo', validators=[DataRequired()])
    submit = SubmitField('Stitch!')
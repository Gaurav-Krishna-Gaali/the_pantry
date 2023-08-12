from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import PasswordInput

class RegistrationForm(FlaskForm):
    username = StringField("What's your name", validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class PasswordForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password = StringField('Password',widget= PasswordInput() ,validators=[DataRequired()])
    submit = SubmitField('Submit')
class AdminForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    password = StringField('Password',widget= PasswordInput() ,validators=[DataRequired()])
    submit = SubmitField('Submit')



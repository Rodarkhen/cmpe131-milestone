# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from datetime import datetime
from .models import User

class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Choose a username"})
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Enter a password"})
    confirm  = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm your password"})
    created_at = DateTimeField('Creation Date', default=datetime.now())
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return 'Username already taken'

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return 'Email already taken'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from datetime import datetime
from app.models import User

# Form for the user to sign up an account
class SignUpForm(FlaskForm):
    # fields used for signup form
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Choose a username"})
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')], render_kw={"placeholder": "Enter a password"})
    confirm  = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm your password"})
    created_at = DateTimeField('Creation Date', default=datetime.now())
    submit = SubmitField('Create Account')

     # Method to check if the username already exist in database
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return 'Username already taken'
        
    # Method to check if the email already exist in database
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return 'Email already taken'

# Form for the user to login to their account
class LoginForm(FlaskForm):
    # Fields declared for the login form
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Form for the user to edit information
class EditProfileForm(FlaskForm):
    # Fields declared for the edit profile form
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    created_at = StringField('Creation Date', render_kw={'readonly': True}) # cannot change, only viewable
    submit = SubmitField('Save Changes')

    # Method to to check if the provided username already exist
    def exist_username(self, field):
        if User.query.filter_by(username=field.data).first():
            return True
    
    # Method to to check if the provided email already exist
    def exist_email(self, field):
        if User.query.filter_by(email=field.data).first():
            return True

# Form for the user to search for a note
class SearchForm(FlaskForm):
    search_query = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Enter Search"})
    submit = SubmitField('Search')

# Form for the user to create a note
class NoteForm(FlaskForm):
    title = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Enter Title"})
    content = TextAreaField('', render_kw={"placeholder": "Enter content"})
    submit = SubmitField('Save Note')
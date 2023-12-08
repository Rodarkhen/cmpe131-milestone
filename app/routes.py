from markupsafe import escape
from flask import render_template
from app import myapp_obj
@myapp_obj.route('/')
@myapp_obj.route('/home')
def home():
    return render_template('home.html')

@myapp_obj.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@myapp_obj.route('/create_note')
def create_note():
    return render_template('create_note.html')
# Add more routes as needed

@myapp_obj.route('/login_page')
def login_page():
    return render_template('login_page.html')


@myapp_obj.route('/logout_feature')
def logout_feature():
    return render_template('/logout_feature.html')

@myapp_obj.route('/API.html')
def API():
    return render_template('/API.html')


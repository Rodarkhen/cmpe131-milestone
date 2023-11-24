#__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

myapp_obj = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(myapp_obj)
login_manager.login_view = 'login'
login_manager.login_message = ('Please log in to access this page.')

basedir = os.path.abspath(os.path.dirname(__file__))

myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(myapp_obj)

with myapp_obj.app_context():
    from app.models import User
    db.create_all()
    
from app import routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
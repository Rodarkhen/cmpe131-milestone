# models.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

# Define the User model for the database
class User(db.Model):
    # Columns that will be on the database for User model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Establish the one-to-many relationship with notes
    notes = db.relationship('Note', backref='user', lazy='dynamic')

    # Method to set the user's password (hashing the password for security)       
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Method to check if a provided password matches the stored hashed
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # String representation of the User object, useful for debugging
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'

    # Method to check if the user is active
    def is_active(self):
        return True
    
    # Method to get the user's ID
    def get_id(self):
        return str(self.id)

    # Method to check if the user is authenticated
    def is_authenticated(self):
        return True
    
    # Method to check if the user is anonymous
    def is_anonymous(self):
        return False
    
    # Method for updating user information (for edit profile)
    def update_info(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
        db.session.commit()


class Note(db.Model):
    # Give each note an ID. This is the primary key for database
    id = db.Column(db.Integer, primary_key=True)
    # Title of note (limited to 100 charecters)
    title = db.Column(db.String(100), nullable=False)
    # Body of the note, stored as text (NO charecter limit)
    content = db.Column(db.Text, nullable=False)
    # Column to store date at which note created
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # User ID that establishes relationship with user ID from other User database
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'

class SharedNote(db.Model):
    # Columns that will be on the database for SharedNote model
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.relationship('Note', backref=db.backref('shared_notes', lazy=True))
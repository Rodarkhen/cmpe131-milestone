# models.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique = True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), unique = True, nullable=False)
    created_at = db.Column(db.DateTime, nullable = False)

    # Establish the one-to-many relationship with notes
    notes = db.relationship('Note', backref='user', lazy='dynamic')
                            
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True 
    def is_anonymous(self):
        return False
    
    # For editing profile
    def update_info(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
        db.session.commit()

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'
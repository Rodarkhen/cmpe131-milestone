# models.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique = True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), unique = True, nullable=False)
    created_at = db.Column(db.DateTime, nullable = False)
    notes = db.relationship('Note')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    
class Note(db.Model):
    #Various "columns" for Note database
    
    id = db.Column(db.Integer, primary_key=True)    #ID for note
    note_title = db.Column(db.String(150))          #Title of note
    data = db.Column(db.String(10000))              #Data or contents of the note
    date = db.Column(db.DateTime(timezone=True), default=func.now())    #Date at which note created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))           #User_ID, which relates to another database
    
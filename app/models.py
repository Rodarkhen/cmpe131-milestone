# models.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(32), unique = True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), unique = True, nullable=False)
    created_at = db.Column(db.DateTime, nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    
    def is_active(self):
        return True  # You can customize this based on your application's logic

    def get_id(self):
        return str(self.id)
    
    def is_authenticated(self):
        return True 
    def is_anonymous(self):
        return False  # Assuming your user objects are not anonymous
    
        # For editing profile
    def update_info(self, name, username, email):
        self.name = name
        self.username = username
        self.email = email
        db.session.commit()
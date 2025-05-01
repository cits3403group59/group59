"""
models.py contains the database models for the application.
It defines the User and UserData models, which are used to store user information and carbon footprint data.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import application

# Initialize database
db = SQLAlchemy(application)

# Creates a User table in database with respective fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    profile_image = db.Column(db.String(100), default='default.png')
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    terms_accepted = db.Column(db.Boolean, default=False)
    
    # Relationship with UserData
    data = db.relationship('UserData', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<User {self.email}>'

# UserData model for storing carbon footprint data
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    carbon_footprint = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<UserData {self.date} - {self.carbon_footprint}>'
    
# UserData model for storing carbon footprint data
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    carbon_footprint = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f'<UserData {self.date} - {self.carbon_footprint}>'

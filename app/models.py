"""
models.py contains the database models for the application.
It defines the User and UserData models, which are used to store user information and carbon footprint data.
"""
from app import db, login_manager  # Import SQLAlchemy instance from __init__.py
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing

# This function is used by Flask-Login to load the user from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association table for accepted friendships (many-to-many)
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

# Creates a User table in database with respective fields
class User(db.Model, UserMixin):
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
    
    # Friends relationship (accepted friends)
    friends = db.relationship(
        'User',
        secondary=friendships,
        primaryjoin=id==friendships.c.user_id,
        secondaryjoin=id==friendships.c.friend_id,
        backref='friend_of'
    )
    # Outgoing and incoming friend requests
    sent_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.sender_id', backref='sender', lazy=True)
    received_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.receiver_id', backref='receiver', lazy=True)
    
    def set_password(self, password: str):
        """Generate and store the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Check if provided password matches stored hash."""
        return check_password_hash(self.password_hash, password)
    
    # Getter method to retrieve the user's friends
    def get_user_friends(self):
        return self.friends
    
    # Method to accept a friend request
    def accept_friend_request(self, request):
        if request.receiver_id != self.id:
            raise ValueError("This friend request is not addressed to this user.")
        
        sender = request.sender
        
        # Add each other as friends (if not already)
        if sender not in self.friends:
            self.friends.append(sender)
            
        # ensure connection is mutual
        if self not in sender.friends:
            sender.friends.append(self)

        # Remove the friend request from the DB
        db.session.delete(request)
        db.session.commit()
        
    def find_friend_by_email(self, email):
        user = User.query.filter_by(email=email).first()  # Find user by email
        if user:
            return user
        return None
        
    def send_friend_request(self, receiver):
        if self.id == receiver.id:
            raise ValueError("You cannot send a friend request to yourself.")
    
        # Check if already friends
        if receiver in self.friends:
            raise ValueError("You are already friends with this user.")
        
        # Check if request already exists (in the other direction)
        existing_request = FriendRequest.query.filter(
            ((FriendRequest.sender_id == self.id) & (FriendRequest.receiver_id == receiver.id)) |
            ((FriendRequest.sender_id == receiver.id) & (FriendRequest.receiver_id == self.id))
        ).first()
        
        if existing_request:
            raise ValueError("Friend already exists between you and this user.")
        
        # create and commit new friend
        request = FriendRequest(sender_id=self.id, receiver_id=receiver.id)
        db.session.add(request)
        db.session.commit()
        
    def deny_friend_request(self, request):
        if request.receiver_id != self.id:
            raise ValueError("You cannot deny a request not addressed to you.")
        db.session.delete(request)
        db.session.commit()

    def cancel_friend_request(self, request):
        if request.sender_id != self.id:
            raise ValueError("You can only cancel requests you sent.")
        db.session.delete(request)
        db.session.commit()

    def remove_friend(self, friend_user):
        if friend_user in self.friends:
            self.friends.remove(friend_user)
            friend_user.friends.remove(self)  # Ensure bidirectional removal
            db.session.commit()
        else:
            raise ValueError("This user is not your friend.")

    def __repr__(self):
        return f'<User {self.email}>'


# UserData model for storing carbon footprint data
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    #carbon_footprint = db.Column(db.Float, nullable=False)
    
    
    # Survey data
    sleep_hours = db.Column(db.Integer, nullable=True)  # Question 1
    coffee_intake = db.Column(db.Integer, nullable=True)  # Question 2
    social_media = db.Column(db.Integer, nullable=True)  # Question 3
    daily_steps = db.Column(db.Integer, nullable=True)  # Question 4
    exercise_minutes = db.Column(db.Integer, nullable=True)  # Question 5
    
    def __repr__(self):
        return f'<UserData {self.date} - {self.carbon_footprint}>'
    
    @classmethod
    def from_form_data(cls,user_id, form_data):
        """
        Creates a new UserData instance from the questionnaire from data
        which is a dictionary from JavaScript.
        """
        return cls(
            user_id = user_id,
            date=datetime.now().date(),
            #carbon_footprint=0.0,
            sleep_hours = int(form_data.get('1')),
            coffee_intake = int(form_data.get('2')),
            social_media = int(form_data.get('3')),
            daily_steps = int(form_data.get('4')),
            exercise_minutes = int(form_data.get('5'))
        )
    
    

# New model for pending friend requests
class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'denied'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FriendRequest from {self.sender_id} to {self.receiver_id} - {self.status}>'



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
        
    def get_data_between(self, start_date=None, end_date=None):
        query = UserData.query.filter_by(user_id=self.id)

        if start_date:
            query = query.filter(UserData.date >= start_date)
        if end_date:
            query = query.filter(UserData.date <= end_date)

        return query.order_by(UserData.date.asc()).all()

    def __repr__(self):
        return f'<User {self.email}>'


# UserData model for storing carbon footprint data
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    #carbon_footprint = db.Column(db.Float, nullable=False)
    
    
     # Survey data - changed to String to store actual text values like "6-8 Hours", "Happy", etc.
    sleep_hours = db.Column(db.String(100), nullable=True)  # Question 1 - stores text like "6-8 Hours"
    coffee_intake = db.Column(db.String(100), nullable=True)  # Question 2 - stores text like "2 Cups"
    social_media = db.Column(db.String(100), nullable=True)  # Question 3 - stores text like "Instagram"
    daily_steps = db.Column(db.String(100), nullable=True)  # Question 4 - stores text like "5001-6000"
    exercise_minutes = db.Column(db.String(100), nullable=True)  # Question 5 - stores text like "31-60 minutes"
    screen_time = db.Column(db.String(100), nullable=True)  # Question 6 - stores text like "2-3 Hours"
    work_time = db.Column(db.String(100), nullable=True)  # Question 7 - stores text like "6-8 Hours"
    study_time = db.Column(db.String(100), nullable=True)  # Question 8 - stores text like "3-4 Hours"
    social_time = db.Column(db.String(100), nullable=True)  # Question 9 - stores text like "1-2 Hours"
    alcohol = db.Column(db.String(100), nullable=True)  # Question 10 - stores text like "Yes" or "No"
    
    # New text input fields (questions 11-15)
    wake_up_time = db.Column(db.String(10), nullable=True)  # Question 11 - time format
    transportation = db.Column(db.String(100), nullable=True)  # Question 12 - text input
    mood = db.Column(db.String(100), nullable=True)  # Question 13 - now stores mood option like "Happy", "Stressed"
    bed_time = db.Column(db.String(10), nullable=True)  # Question 14 - time format
    money_spent = db.Column(db.Float, nullable=True)  # Question 15 - float with 2 decimal places
    
    
    
    def __repr__(self):
        return f'<UserData {self.date} - {self.carbon_footprint}>'
    
    @classmethod
    def from_form_data(cls, user_id, form_data):
        """
        Creates a new UserData instance from the questionnaire form data
        which is a dictionary from JavaScript.
        
        Now handles the text values properly for all questions.
        """
        selected_date = datetime.strptime(form_data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        
        # Handle money spent - ensure it's a float with 2 decimal places
        money_spent_value = form_data.get('15')
        if money_spent_value:
            try:
                money_spent = float(money_spent_value)
                money_spent = round(money_spent, 2)  # Ensure exactly 2 decimal places
            except ValueError:
                money_spent = None
        else:
            money_spent = None
        
        return cls(
            user_id=user_id,
            date=selected_date,
            # All these now store the actual text values
            sleep_hours=str(form_data.get('1', '')) if form_data.get('1') else None,
            coffee_intake=str(form_data.get('2', '')) if form_data.get('2') else None,
            social_media=str(form_data.get('3', '')) if form_data.get('3') else None,
            daily_steps=str(form_data.get('4', '')) if form_data.get('4') else None,
            exercise_minutes=str(form_data.get('5', '')) if form_data.get('5') else None,
            screen_time=str(form_data.get('6', '')) if form_data.get('6') else None,
            work_time=str(form_data.get('7', '')) if form_data.get('7') else None,
            study_time=str(form_data.get('8', '')) if form_data.get('8') else None,
            social_time=str(form_data.get('9', '')) if form_data.get('9') else None,
            alcohol=str(form_data.get('10', '')) if form_data.get('10') else None,
            wake_up_time=form_data.get('11'),
            transportation=form_data.get('12'),
            mood=str(form_data.get('13', '')) if form_data.get('13') else None,  # Now stores mood text like "Happy"
            bed_time=form_data.get('14'),
            money_spent=money_spent
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



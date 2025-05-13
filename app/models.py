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
    
    # Numeric fields with appropriate data types
    sleep_hours = db.Column(db.Float, nullable=True)  # Question 1 - decimal hours (0-24)
    coffee_intake = db.Column(db.Integer, nullable=True)  # Question 2 - integer cups
    social_media = db.Column(db.String(100), nullable=True)  # Question 3 - categorical (Instagram, YouTube, etc.)
    daily_steps = db.Column(db.Integer, nullable=True)  # Question 4 - integer steps
    exercise_hours = db.Column(db.Float, nullable=True)  # Question 5 - decimal hours (renamed from exercise_minutes)
    screen_time = db.Column(db.Float, nullable=True)  # Question 6 - decimal hours
    work_time = db.Column(db.Float, nullable=True)  # Question 7 - decimal hours
    study_time = db.Column(db.Float, nullable=True)  # Question 8 - decimal hours
    social_time = db.Column(db.Float, nullable=True)  # Question 9 - decimal hours
    alcohol = db.Column(db.Integer, nullable=True)  # Question 10 - integer drinks
    
    # Text input fields
    wake_up_time = db.Column(db.String(10), nullable=True)  # Question 11 - time format
    transportation = db.Column(db.String(100), nullable=True)  # Question 12 - categorical
    mood = db.Column(db.String(100), nullable=True)  # Question 13 - categorical
    bed_time = db.Column(db.String(10), nullable=True)  # Question 14 - time format
    money_spent = db.Column(db.Float, nullable=True)  # Question 15 - decimal currency    
    
    def __repr__(self):
        return f'<UserData {self.date} - {self.carbon_footprint}>'
    
    @classmethod
    def from_form_data(cls, user_id, form_data):
        """
        Creates a new UserData instance from the questionnaire form data
        which is a dictionary from JavaScript.
        
        Properly converts input to appropriate data types based on the updated schema.
        """
        selected_date = datetime.strptime(form_data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        
        # Process numeric fields
        numeric_fields = {
            '1': 'float',    # sleep_hours (decimal hours)
            '2': 'int',      # coffee_cups (integer)
            '4': 'int',      # daily_steps (integer)
            '5': 'float',    # exercise_hours (decimal hours)
            '6': 'float',    # screen_time (decimal hours)
            '7': 'float',    # work_time (decimal hours)
            '8': 'float',    # study_time (decimal hours)
            '9': 'float',    # social_time (decimal hours)
            '10': 'int'      # alcohol (integer cups)
        }
        
        # Convert fields to proper types
        processed_data = {}
        
        for field, field_type in numeric_fields.items():
            if field in form_data and form_data[field]:
                try:
                    if field_type == 'int':
                        processed_data[field] = int(float(form_data[field]))
                    elif field_type == 'float':
                        processed_data[field] = round(float(form_data[field]), 1)  # 1 decimal place
                except (ValueError, TypeError):
                    processed_data[field] = None
            else:
                processed_data[field] = None
        
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
            sleep_hours=processed_data.get('1'),
            coffee_intake=processed_data.get('2'),
            social_media=form_data.get('3'),
            daily_steps=processed_data.get('4'),
            exercise_hours=processed_data.get('5'),  # Now using exercise_hours instead of exercise_minutes
            screen_time=processed_data.get('6'),
            work_time=processed_data.get('7'),
            study_time=processed_data.get('8'),
            social_time=processed_data.get('9'),
            alcohol=processed_data.get('10'),
            wake_up_time=form_data.get('11'),
            transportation=form_data.get('12'),
            mood=form_data.get('13'),
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



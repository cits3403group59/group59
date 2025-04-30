# # app.py - Main Flask application file
# from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# from datetime import datetime
# 
# # Initialize Flask app
# app = Flask(__name__)
# 
# # Enable CORS so that the frontend Javascript can make requests to backend even if it is running from another
# # domain or port
# CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
# 
# # Configure database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_copy.db'  # SQLite for simplicity
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production!
# 
# # Set a specific password hashing method that works on older Python versions
# app.config['WERKZEUG_DEFAULT_PASSWORD_HASH'] = 'pbkdf2:sha256:150000'
# 
# # Initialize database
# db = SQLAlchemy(app)
# 
# # Creates a User table in database with respective fields
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128), nullable=False)
#     dob = db.Column(db.Date, nullable=False)
#     profile_image = db.Column(db.String(100), default='default.png')
#     joined_date = db.Column(db.DateTime, default=datetime.utcnow)
#     terms_accepted = db.Column(db.Boolean, default=False)
#     
#     # Relationship with UserData
#     data = db.relationship('UserData', backref='user', lazy=True, cascade="all, delete-orphan")
#     
#     def __repr__(self):
#         return f'<User {self.email}>'
# 
# # UserData model for storing carbon footprint data
# class UserData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     carbon_footprint = db.Column(db.Float, nullable=False)
#     
#     def __repr__(self):
#         return f'<UserData {self.date} - {self.carbon_footprint}>'
# 
# # # Basic routes for serving HTML pages
# # @app.route('/')
# # def home():
# #     # Check if user is logged in
# #     if 'user_id' in session:
# #         # User is logged in, serve logged-in version
# #         return send_from_directory('.', 'static-introductory-loggedin.html')
# #     else:
# #         # User is not logged in, serve not-logged-in version
# #         return send_from_directory('.', 'static-introductory-notloggedin.html')
# # 
# # @app.route('/login')
# # def login_page():
# #     # If user is already logged in, redirect to home
# #     if 'user_id' in session:
# #         return redirect(url_for('home'))
# #     return send_from_directory('.', 'login.html')
# # 
# # @app.route('/signup')
# # def signup_page():
# #     # If user is already logged in, redirect to home
# #     if 'user_id' in session:
# #         return redirect(url_for('home'))
# #     return send_from_directory('.', 'signup.html')
# # 
# # @app.route('/dashboard')
# # def dashboard():
# #     # Only allow access if user is logged in
# #     if 'user_id' not in session:
# #         return redirect(url_for('login_page'))
# #     return send_from_directory('.', 'static-introductory-loggedin.html')
# 
# @app.route('/logout')
# def logout():
#     # Clear the session
#     session.pop('user_id', None)
#     return redirect(url_for('home'))
# 
# # Authentication routes
# @app.route('/api/auth/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     
#     # Print received data for debugging
#     print("Received registration data:", data)
#     
#     # Extract fields
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')
#     password = data.get('password')
#     dob_str = data.get('dob')
#     terms_accepted = data.get('terms_accepted', False)
#     
#     # Validate required fields
#     if not all([first_name, last_name, email, password, dob_str]):
#         missing = []
#         if not first_name: missing.append('first_name')
#         if not last_name: missing.append('last_name')
#         if not email: missing.append('email')
#         if not password: missing.append('password')
#         if not dob_str: missing.append('dob')
#         return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
#     
#     if not terms_accepted:
#         return jsonify({"error": "You must accept the terms and conditions"}), 400
#     
#     # Validate and convert dob
#     try:
#         dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"error": "Invalid date of birth format"}), 400
#     
#     # Check if email is already registered
#     if User.query.filter_by(email=email).first():
#         return jsonify({"error": "Email already registered"}), 400
#     
#     # Create and store user
#     try:
#         # Explicitly use a compatible hashing method
#         hashed_password = generate_password_hash(
#             password, 
#             method='pbkdf2:sha256', 
#             salt_length=8
#         )
#         
#         new_user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password_hash=hashed_password,
#             dob=dob,
#             terms_accepted=terms_accepted
#         )
#         
#         db.session.add(new_user)
#         db.session.commit()
#         
#         return jsonify({
#             "message": "User registered successfully",
#             "user": {
#                 "id": new_user.id,
#                 "firstName": new_user.first_name,
#                 "lastName": new_user.last_name,
#                 "email": new_user.email
#             }
#         }), 201
#     except Exception as e:
#         db.session.rollback()
#         print("Error during registration:", str(e))
#         return jsonify({"error": str(e)}), 500
# 
# @app.route('/api/auth/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     
#     # Print received data for debugging
#     print("Received login data:", data)
#     
#     # Extract fields
#     email = data.get('email')
#     password = data.get('password')
#     remember = data.get('remember', False)
#     
#     # Validate required fields
#     if not all([email, password]):
#         return jsonify({"error": "Email and password are required"}), 400
#     
#     # Find user by email
#     user = User.query.filter_by(email=email).first()
#     
#     # Check if user exists and password is correct
#     if not user or not check_password_hash(user.password_hash, password):
#         return jsonify({"error": "Invalid email or password"}), 401
#     
#     # Create session
#     session['user_id'] = user.id
#     session.permanent = remember
#     
#     return jsonify({
#         "message": "Login successful",
#         "user": {
#             "id": user.id,
#             "firstName": user.first_name,
#             "lastName": user.last_name,
#             "email": user.email
#         }
#     }), 200
# 
# # API endpoint to get current user info
# @app.route('/api/auth/user', methods=['GET'])
# def get_current_user():
#     if 'user_id' not in session:
#         return jsonify({"error": "Not logged in"}), 401
#     
#     user = User.query.get(session['user_id'])
#     if not user:
#         # Clear invalid session
#         session.pop('user_id', None)
#         return jsonify({"error": "User not found"}), 404
#     
#     return jsonify({
#         "user": {
#             "id": user.id,
#             "firstName": user.first_name,
#             "lastName": user.last_name,
#             "email": user.email
#         }
#     }), 200
# 
# # Create database tables when app runs for the first time
# with app.app_context():
#     db.create_all()
#     
# from routes import *
# 
# if __name__ == '__main__':
#     app.run(debug=True)
"""
Routes for authentication.
"""
from . import auth

from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms import SignUpForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from flask import session
from werkzeug.security import check_password_hash
from app.forms import SignInForm

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            dob=form.dob.data,
            password_hash=hashed_password,
            terms_accepted=form.terms_accepted.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup_page.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        # Find user by email
        user = User.query.filter_by(email=email).first()

        # Check if user exists and password is correct
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session.permanent = remember
            flash('Login successful!', 'success')
            return redirect(url_for('main.introductory'))  
        flash('Invalid email or password.', 'danger')

    return render_template('login_page.html', form=form)

# from flask-login import login_user, logout_user
# from flask import request, jsonify, session, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# from app import application, db
# from app.models import User

# @application.route('/register', methods=['GET', 'POST'])
# def register():
#     data = request.get_json()
    
#     print("Received registration data:", data)
    
#     # Extract fields
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')
#     password = data.get('password')
#     dob_str = data.get('dob')
#     terms_accepted = data.get('terms_accepted', False)
    
#     # Validate required fields
#     if not all([first_name, last_name, email, password, dob_str]):
#         missing = []
#         if not first_name: missing.append('first_name')
#         if not last_name: missing.append('last_name')
#         if not email: missing.append('email')
#         if not password: missing.append('password')
#         if not dob_str: missing.append('dob')
#         return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
    
#     if not terms_accepted:
#         return jsonify({"error": "You must accept the terms and conditions"}), 400
    
#     # Validate and convert dob
#     try:
#         dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
#     except ValueError:
#         return jsonify({"error": "Invalid date of birth format"}), 400
    
#     # Check if email is already registered
#     if User.query.filter_by(email=email).first():
#         return jsonify({"error": "Email already registered"}), 400
    
#     # Create and store user
#     try:
#         # Explicitly use a compatible hashing method
#         hashed_password = generate_password_hash(
#             password, 
#             method='pbkdf2:sha256', 
#             salt_length=8
#         )
        
#         new_user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password_hash=hashed_password,
#             dob=dob,
#             terms_accepted=terms_accepted
#         )
        
#         # add user to the database and commit (push changes)
#         db.session.add(new_user)
#         db.session.commit()
        
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
    
# @application.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
    
#     # Print received data for debugging
#     print("Received login data:", data)
    
#     # Extract fields
#     email = data.get('email')
#     password = data.get('password')
#     remember = data.get('remember', False)
    
#     # Validate required fields
#     if not all([email, password]):
#         return jsonify({"error": "Email and password are required"}), 400
    
#     # Find user by email
#     user = User.query.filter_by(email=email).first()
    
#     # Check if user exists and password is correct
#     if not user or not check_password_hash(user.password_hash, password):
#         return jsonify({"error": "Invalid email or password"}), 401
    
#     # Create session
#     session['user_id'] = user.id
#     session.permanent = remember
    
#     return jsonify({
#         "message": "Login successful",
#         "user": {
#             "id": user.id,
#             "firstName": user.first_name,
#             "lastName": user.last_name,
#             "email": user.email
#         }
#     }), 200

# # route for logout
# @application.route('/logout', methods=['POST'])
# def logout():
#     logout_user()
#     return redirect(url_for('introductory'))


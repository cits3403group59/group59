"""
Routes for authentication.
"""
from . import auth

from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm, SignInForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from flask import session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user


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

# def login():
#     print("\n--- Entering login route ---") # Debug print

#     form = SignInForm()
    
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         remember = form.remember.data

#         print(f"Attempting login for email: {email}") # Debug print

#         # Find user by email
#         user = User.query.filter_by(email=email).first()
        
#         print(f"User found in DB: {user is not None}") # Debug print
        
#         # Check if user exists and password is correct
#         if user and check_password_hash(user.password_hash, password):
#             # Log the user in and set the remember option
#             login_user(user, remember=remember)
#             flash('Login successful!', 'success')
            
#             # Store user ID in session
#             #session['user_id'] = user.id  
            
#             return redirect(url_for('main.introductory'))
        
#         flash('Invalid email or password.', 'danger')
    
#     return render_template('login_page.html', form=form)

def try_to_login_user(email, password):
    user = User.query.filter_by(email=email).first()
    
    if user:
        if user.check_password(password):
            return user
        elif not user.check_password(password):
            return 'Wrong Password'
        
    if not user:
        print("User does not exist")
        return 'User does not exist'
    
    return None

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    
    if request.method == "POST":
        print("\n--- Entering login route ---") # Debug print

        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        print(f"Attempting login for email: {email}") # Debug print

        result = try_to_login_user(email, password)
        if isinstance(result, User):
            login_user(result, remember=remember)
            return redirect(url_for('main.introductory'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login_page.html', form=form)

@auth.route('/logout')
def logout():  
    if 'user_id' in session: 
        logout_user()
        flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

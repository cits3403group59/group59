"""
Routes for authentication.
"""
from . import auth

from flask import render_template, redirect, url_for, flash, request
from app.forms import SignUpForm
from app.models import User
from app import db
from werkzeug.security import generate_password_hash
from flask import session
from werkzeug.security import check_password_hash
from flask_login import login_user

from app.forms import SignInForm
from flask_login import logout_user

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
            # Log the user in and set the remember option
            login_user(user, remember=remember)
            flash('Login successful!', 'success')
            
            # Store user ID in session
            session['user_id'] = user.id  
            
            return redirect(url_for('main.introductory'))
        
        flash('Invalid email or password.', 'danger')
    
    return render_template('login_page.html', form=form)

@auth.route('/logout')
def logout():  
    if 'user_id' in session: 
        logout_user()
        flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
from flask import render_template, redirect, url_for, session
from app import application
from flask import request, jsonify, send_from_directory

# Route for the introductory page
@application.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the login page
@application.route('/login')
def login():
    return render_template('login-page.html')

# Route for the account creation page
@application.route('/signup')
def signup():
    return render_template('signup-page.html')

# Route for the visualise data page
@application.route('/visualise-my-data')
def vis_my_data():
    return render_template('visualise-my-data.html') 

# Route for the visualise twin data page
@application.route('/visualise-twin-data')
def vis_twin_data():
    return render_template('visualise-twin-data.html')

# Route for the visualise friend data page
@application.route('/visualise-friend-data')
def vis_friend_data():
    return render_template('visualise-friend-data.html')

# Route for upload data page
@application.route('/upload-data')
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@application.route('/manual-data')
def manual_data():
    return render_template('manual-data.html')

# Route for settings page
@application.route('/settings')
def settings():
    return render_template('settings.html')

# Route for share data page
@application.route('/share-data')
def share_data():
    return render_template('share-data.html')

"""
TODO: 
- these are taking you to static HTML files
- there is not currently differemt versions of the home page for logged in and out 
- THIS WILL PROBABLY THROW AN ERROR SINCE SOME OF THESE HTML FILES DO NOT EXIST
"""

# Basic routes for serving HTML pages
@application.route('/')
def home():
    # Check if user is logged in
    if 'user_id' in session:
        # User is logged in, serve logged-in version
        return send_from_directory('.', 'static-introductory-loggedin.html')
    else:
        # User is not logged in, serve not-logged-in version
        return send_from_directory('.', 'static-introductory-notloggedin.html')

@application.route('/login')
def login_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('home'))
    return send_from_directory('.', 'login.html')

@application.route('/signup')
def signup_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('home'))
    return send_from_directory('.', 'signup.html')

@application.route('/dashboard')
def dashboard():
    # Only allow access if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return send_from_directory('.', 'static-introductory-loggedin.html')

@application.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    return redirect(url_for('home'))

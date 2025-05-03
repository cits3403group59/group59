"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
from flask import render_template, redirect, url_for, session
from app import application

# Route for the introductory page
@application.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the visualise data page
@application.route('/visualise-my-data')
def vis_my_data():
    return render_template('visualise_my_data.html') 

# Route for the visualise twin data page
@application.route('/visualise-twin-data')
def vis_twin_data():
    return render_template('visualise_twin_data.html')

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

@application.route('/login')
def login_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('introductory'))
    return render_template('login_page.html')

@application.route('/signup')
def signup_page():
    # If user is already logged in, redirect to home
    if 'user_id' in session:
        return redirect(url_for('introductory'))
    return render_template('signup_page.html')

@application.route('/logout')
def logout():
    # Clear the session
    session.pop('user_id', None)
    return redirect(url_for('introductory'))


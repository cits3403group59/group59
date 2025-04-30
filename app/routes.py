"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
from flask import render_template, redirect, url_for, session
from app import app

# Route for the introductory page
@app.route('/')
def introductory():
    return render_template('introductory.html')

# Route for the login page
@app.route('/login')
def login():
    return render_template('login-page.html')

# Route for the account creation page
@app.route('/signup')
def signup():
    return render_template('signup-page.html')

# Route for the visualise data page
@app.route('/visualise-my-data')
def vis_my_data():
    return render_template('visualise-my-data.html') 

# Route for the visualise twin data page
@app.route('/visualise-twin-data')
def vis_twin_data():
    return render_template('visualise-twin-data.html')

# Route for the visualise friend data page
@app.route('/visualise-friend-data')
def vis_friend_data():
    return render_template('visualise-friend-data.html')

# Route for upload data page
@app.route('/upload-data')
def upload_data():
    return render_template('upload-data-page.html')

# Route for manual data page
@app.route('/manual-data')
def manual_data():
    return render_template('manual-data.html')

# Route for settings page
@app.route('/settings')
def settings():
    return render_template('settings.html')

# Route for share data page
@app.route('/share-data')
def share_data():
    return render_template('share-data.html')


# Run the application
if __name__ == '__main__':
    app.run()
"""
A python file containing the routes for the Flask application.

Contains all request handlers.
"""
from flask import render_template
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


# Route for the upload data page
@app.route('/upload-data')
def upload_data():
    return render_template('upload-data-page.html')

# Run the application
if __name__ == '__main__':
    app.run()
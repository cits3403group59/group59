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

# Run the application
if __name__ == '__main__':
    app.run()
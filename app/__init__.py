"""
This python fule contains a Flaks application instances 
"""

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temporary_secret_key'  # Replace with a secure key in production

from app import routes 
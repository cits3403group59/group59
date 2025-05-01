"""
This file contains the initialization code for the Carbon Copy application.
It sets up the Flask application, and imports the routes.
"""
from flask import Flask

application = Flask(__name__)

from app import routes 


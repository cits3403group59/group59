"""
This module contains the configuration settings for the application.
It includes settings for the database, CORS, and other application-specific configurations.
"""

# app.py - Main Flask application file
from flask import Flask, request, jsonify, session, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

from app import application # import the application instance from __init__.py

# Enable CORS so that the frontend Javascript can make requests to backend even if it is running from another
# domain or port
CORS(application, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configure database
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production!
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_copy.db'  # SQLite for simplicity

# Set a specific password hashing method that works on older Python versions
application.config['WERKZEUG_DEFAULT_PASSWORD_HASH'] = 'pbkdf2:sha256:150000'
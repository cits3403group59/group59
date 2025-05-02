"""
This file contains the initialization code for the Carbon Copy application.
It sets up the Flask application, and imports the routes.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Create application instance
application = Flask(__name__)

# Configure application
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production!
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_copy.db'  # SQLite for simplicity
application.config['WERKZEUG_DEFAULT_PASSWORD_HASH'] = 'pbkdf2:sha256:150000'

# Setup CORS
CORS(application, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize database
db = SQLAlchemy(application)
migrate = Migrate(application, db)

# Import routes AFTER application and db are created - this prevents circular imports
from app import routes, auth, models
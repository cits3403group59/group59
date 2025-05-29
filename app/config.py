"""
This module contains the configuration settings for the application.
"""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, '..', 'instance')  # path to instance/

# Absolute path to DB file in instance/
default_db_path = 'sqlite:///' + os.path.join(instance_dir, 'carbon_copy.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') #
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 29.05 (post project submission): commenting this out to demonstrat app login functionality 
    # REMEMBER_COOKIE_DURATION = timedelta(hours=1)  # Keep user logged in for 1 hour
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'profile_pics')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # Limit upload size to 2MB
    
#my addition    
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'  # Use in-memory database
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

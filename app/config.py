"""
This module contains the configuration settings for the application.
It includes settings for the database, CORS, and other application-specific configurations.
"""
import os
from app import application # import the application instance from __init__.py

basedir = os.path.abspath(os.path.dirname(__file__))
default_db_path = 'sqlite://'+os.path.join(basedir, 'carbon_copy.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_db_path
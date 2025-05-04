"""
This module contains the configuration settings for the application.
It includes settings for the database, CORS, and other application-specific configurations.
"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, '..', 'instance')  # path to instance/

# Absolute path to DB file in instance/
default_db_path = 'sqlite:///' + os.path.join(instance_dir, 'carbon_copy.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'  # change this later
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or default_db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False

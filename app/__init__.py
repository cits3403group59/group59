"""
This file contains the initialization code for the Carbon Copy application.
It sets up the Flask application, and imports the routes.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_object=None):
    app = Flask(__name__)
    #app.config.from_object('app.config.Config')
    
    # Use the provided config_object or default to Config
    if config_object is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # automatically redirect to login page if user is not logged in
    csrf = CSRFProtect(app)

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

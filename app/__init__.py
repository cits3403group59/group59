"""
This file contains the initialization code for the Carbon Copy application.
It sets up the Flask application, and imports the routes.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app


# # Configure application
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# application.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production!
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_copy.db'  # SQLite for simplicity
# application.config['WERKZEUG_DEFAULT_PASSWORD_HASH'] = 'pbkdf2:sha256:150000'

# # Setup CORS
# CORS(application, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# # Initialize database
# db = SQLAlchemy(application)
# migrate = Migrate(application, db)


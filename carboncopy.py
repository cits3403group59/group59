"""
This python file is the main application module.
"""
from app import application, db

# Create database tables when app runs for the first time
with application.app_context():
    db.create_all()

if __name__ == '__main__':
    application.run() 
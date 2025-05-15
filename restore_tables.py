# restore_tables.py - This is just a local script, don't commit it to Git
from app import create_app, db
from sqlalchemy import inspect

app = create_app()  # This uses your regular app configuration

with app.app_context():
    # Create all tables defined in your models
    db.create_all()
    
    # Verify the tables were created - using inspector instead of table_names()
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables created: {tables}")
    
    # Add a message showing the database location
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
from app import application, db

if __name__ == "__main__":
    # Create all database tables
    with application.app_context():
        db.create_all()
    # Run the application
    application.run(debug=True)
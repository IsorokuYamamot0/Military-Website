from app import app, db

if __name__ == '__main__':
    # Use app_context to create database tables before running the app
    with app.app_context():
        db.create_all()
    # Run the Flask development server
    app.run(debug=True)

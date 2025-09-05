# This website is made by Nishil Singh June 1 2025
# Whole Python file was from peices of last year project and from help from a classmate.
# Import the 'app' and 'db'
from app import app, db

# This block ensures that the following code runs only when the script is executed directly
# and not when it's imported into another script.
if __name__ == '__main__':
    # Use app_context to create database tables before running the app
    with app.app_context():
        db.create_all()
    # Run the Flask development server
    app.run(debug=True)

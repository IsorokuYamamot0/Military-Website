from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "USA.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import routes and models *after* initializing app and db to avoid circular imports
from app import routes, models


# Define a function to create the database tables
def create_tables():
    with app.app_context():
        db.create_all()


# Register a command-line command to initialize the database
@app.cli.command('init-db')
def init_db_command():
    """Creates the database tables."""
    create_tables()
    print('Initialized the database.')
# Ensure the app runs when this script is executed


if __name__ == '__main__':
    app.run(debug=True)

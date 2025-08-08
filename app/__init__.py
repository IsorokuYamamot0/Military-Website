from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create the Flask application instance
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "USA_vehicles.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# A secret key is required for session management and flash messages.
app.config['SECRET_KEY'] = 'your_secret_key'  # This should be a complex, random value in a real application.

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes and models to link them to the app
# This import is at the end to avoid circular dependencies
from app import routes, models

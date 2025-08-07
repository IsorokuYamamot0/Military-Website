from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Create the Flask application instance
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "USA_vehicles.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import routes and models to link them to the app
# This import is at the end to avoid circular dependencies
from app import routes, models

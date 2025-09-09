# This website is made by Nishil Singh June 1 2025

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager # Import LoginManager

# Create the Flask application instance
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "USA_vehicles.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Had ai help with this and make this secret key.
# A secret key is required for session management and flash messages.
app.config['SECRET_KEY'] = 'Rocky_4730_Nishil_2008'  # This should be a complex, random value in a real application.

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Specify the login view

# Import routes and models to link them to the app
# This import is at the end to avoid circular dependencies
from app import routes, models

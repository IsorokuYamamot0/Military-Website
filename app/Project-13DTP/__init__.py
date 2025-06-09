from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///military.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import routes after creating app to avoid circular import
    with app.app_context():
        from . import routes
        from .models import Plane, Tank, ICBM, Helicopter, AirGroundMissile, SurfaceMissile, SeaSurfaceMissile
        db.create_all()

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///military.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Add secret key for sessions
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    with app.app_context():
        from . import routes  # Import routes
        from .models import Plane, Tank, ICBM, Helicopter, AirGroundMissile, SurfaceMissile, SeaSurfaceMissile
        
        # Create all tables
        db.create_all()
        
        # Register error handlers
        @app.errorhandler(404)
        def not_found_error(error):
            return app.send_static_file('404.html'), 404
            
        @app.errorhandler(500)
        def internal_error(error):
            db.session.rollback()
            return app.send_static_file('500.html'), 500

    return app
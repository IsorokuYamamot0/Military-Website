# This website is made by Nishil Singh June 1 2025

from app import db


class Tank(db.Model):
    """Represents a tank in the database."""
    __tablename__ = 'tank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    year_introduced = db.Column(db.Integer)
    # Add a 'type' field for consistent display in templates
    type = db.Column(db.String(50), default='Tank')

    def __repr__(self):
        return f"<Tank {self.name}>"


class Plane(db.Model):
    """Represents a plane in the database."""
    __tablename__ = 'plane'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50))
    description = db.Column(db.Text)
    # Add a 'type' field for consistent display in templates
    type = db.Column(db.String(50), default='Aircraft')

    def __repr__(self):
        return f"<Plane {self.name}>"

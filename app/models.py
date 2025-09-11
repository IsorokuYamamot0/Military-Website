
# This website is made by Nishil Singh June 1 2025

from app import db
from flask_login import UserMixin # Import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing

# Association table for the many-to-many relationship between Tank and Country
# It links tanks to the countries that operate them.
tank_countries = db.Table('tank_countries',
    db.Column('tank_id', db.Integer, db.ForeignKey('tank.id'), primary_key=True),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True)
)

# Association table for the many-to-many relationship between Plane and Country
# It links planes to the countries that operate them.
plane_countries = db.Table('plane_countries',
    db.Column('plane_id', db.Integer, db.ForeignKey('plane.id'), primary_key=True),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True)
)

# New association table for user favorites (Tanks)
user_favorite_tanks = db.Table('user_favorite_tanks',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tank_id', db.Integer, db.ForeignKey('tank.id'), primary_key=True)
)

# New association table for user favorites (Planes)
user_favorite_planes = db.Table('user_favorite_planes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('plane_id', db.Integer, db.ForeignKey('plane.id'), primary_key=True)
)

# This was made from ai help and the page.


class Country(db.Model):
    """Represents a country that operates military vehicles."""
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Country {self.name}>"
# This was made from me and the ai help, then I replecated it to the plane class.


class Tank(db.Model):
    """Represents a tank in the database."""
    __tablename__ = 'tank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    year_introduced = db.Column(db.Integer)
    type = db.Column(db.String(50), default='Tank')
    # New field for external link
    external_link = db.Column(db.String(500), nullable=True) # Max length 500, can be empty

    countries = db.relationship('Country', secondary=tank_countries, lazy=True,
                                backref=db.backref('tanks', lazy=True))

    def __repr__(self):
        return f"<Tank {self.name}>"


class Plane(db.Model):
    """Represents a plane in the database."""
    __tablename__ = 'plane'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(50))
    description = db.Column(db.Text)
    type = db.Column(db.String(50), default='Aircraft')
    # New field for external link
    external_link = db.Column(db.String(500), nullable=True) # Max length 500, can be empty

    countries = db.relationship('Country', secondary=plane_countries, lazy=True,
                                backref=db.backref('planes', lazy=True))

    def __repr__(self):
        return f"<Plane {self.name}>"

# New User model for authentication


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) # New field for admin status

    # Many-to-many relationship for favorited tanks
    favorite_tanks = db.relationship('Tank', secondary=user_favorite_tanks, lazy=True,
                                     backref=db.backref('favorited_by_users', lazy=True))
    # Many-to-many relationship for favorited planes
    favorite_planes = db.relationship('Plane', secondary=user_favorite_planes, lazy=True,
                                      backref=db.backref('favorited_by_users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

# This website is made by Nishil Singh June 1 2025

from app import db

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

class Country(db.Model):
    """Represents a country that operates military vehicles."""
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Country {self.name}>"

class Tank(db.Model):
    """Represents a tank in the database."""
    __tablename__ = 'tank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    year_introduced = db.Column(db.Integer)
    # Add a 'type' field for consistent display in templates
    type = db.Column(db.String(50), default='Tank')

    # Many-to-many relationship with Country
    # 'secondary' specifies the association table
    # 'backref' allows access to tanks from a country object
    # 'lazy=True' means the related objects are loaded when accessed
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
    # Add a 'type' field for consistent display in templates
    type = db.Column(db.String(50), default='Aircraft')

    # Many-to-many relationship with Country
    # 'secondary' specifies the association table
    # 'backref' allows access to planes from a country object
    # 'lazy=True' means the related objects are loaded when accessed
    countries = db.relationship('Country', secondary=plane_countries, lazy=True,
                                backref=db.backref('planes', lazy=True))

    def __repr__(self):
        return f"<Plane {self.name}>"
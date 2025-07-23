from app import db

# Association Tables (Many-to-Many)
country_tank = db.Table('country_tank',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('tank_id', db.Integer, db.ForeignKey('tank.id'))
)

country_plane = db.Table('country_plane',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('plane_id', db.Integer, db.ForeignKey('plane.id'))
)

country_missile = db.Table('country_missile',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id')),
    db.Column('missile_id', db.Integer, db.ForeignKey('missile.id'))
)


# Main Models
class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    tanks = db.relationship('Tank', secondary=country_tank, back_populates='countries')
    planes = db.relationship('Plane', secondary=country_plane, back_populates='countries')
    missiles = db.relationship('Missile', secondary=country_missile, back_populates='countries')

    def __repr__(self):
        return f"<Country {self.name}>"


class Tank(db.Model):
    __tablename__ = 'tank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    year_introduced = db.Column(db.Integer)

    countries = db.relationship('Country', secondary=country_tank, back_populates='tanks')

    def __repr__(self):
        return f"<Tank {self.name}>"


class Plane(db.Model):
    __tablename__ = 'plane'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))  # e.g., Fighter, Bomber, Recon
    description = db.Column(db.Text)

    countries = db.relationship('Country', secondary=country_plane, back_populates='planes')

    def __repr__(self):
        return f"<Plane {self.name}>"


class Missile(db.Model):
    __tablename__ = 'missile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    missile_type = db.Column(db.String(50))  # e.g., ICBM, Cruise, Anti-Air
    range_km = db.Column(db.Integer)
    description = db.Column(db.Text)

    countries = db.relationship('Country', secondary=country_missile, back_populates='missiles')

    def __repr__(self):
        return f"<Missile {self.name}>"

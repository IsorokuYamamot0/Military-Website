from . import db


class WeaponBase(db.Model):
    __abstract__ = True

    @property
    def name(self):
        return getattr(self, 'Name', getattr(self, 'Tank_Name', getattr(self, 'ICBM_Name', getattr(self, 'Heli_Name', 'Unknown')))) or f'Unknown {self.type}'

    @property
    def country(self):
        return getattr(self, 'Country', 'Unknown') or 'Unknown'

    def __repr__(self):
        return f'<{self.type} {self.name}>'


class Plane(WeaponBase):
    __tablename__ = 'planes'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Aircraft'


class Tank(WeaponBase):
    __tablename__ = 'tanks'
    id = db.Column(db.Integer, primary_key=True)
    Tank_Name = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Tank'


class ICBM(WeaponBase):
    __tablename__ = 'icbm'
    id = db.Column(db.Integer, primary_key=True)
    ICBM_Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'ICBM'


class Helicopter(WeaponBase):
    __tablename__ = 'helicopters'
    id = db.Column(db.Integer, primary_key=True)
    Heli_Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Helicopter'


class AirGroundMissile(WeaponBase):
    __tablename__ = 'air_ground_missiles'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Air-to-Ground Missile'


class SurfaceMissile(WeaponBase):
    __tablename__ = 'surface_missiles'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Surface Missile'


class SeaSurfaceMissile(WeaponBase):
    __tablename__ = 'sea_surface_missiles'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)

    @property
    def type(self):
        return 'Sea-to-Surface Missile'

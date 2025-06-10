from . import db

class Plane(db.Model):
    __tablename__ = 'Planes'
    id_planes = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Name or 'Unknown Aircraft'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property 
    def type(self):
        return 'Aircraft'

    def __repr__(self):
        return f'<Plane {self.Name}>'

class Tank(db.Model):
    __tablename__ = 'Tanks'
    id_Tanks = db.Column(db.Integer, primary_key=True)
    Tank_Name = db.Column(db.String(100), nullable=False)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Tank_Name or 'Unknown Tank'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'Tank'

    def __repr__(self):
        return f'<Tank {self.Tank_Name}>'

class ICBM(db.Model):
    __tablename__ = 'ICBM'
    id_ICBM = db.Column(db.Integer, primary_key=True)
    ICBM_Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.ICBM_Name or 'Unknown ICBM'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'ICBM'

    def __repr__(self):
        return f'<ICBM {self.ICBM_Name}>'

class Helicopter(db.Model):
    __tablename__ = 'Helicopter'
    id_Heli = db.Column(db.Integer, primary_key=True)
    Heli_Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Heli_Name or 'Unknown Helicopter'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'Helicopter'

    def __repr__(self):
        return f'<Helicopter {self.Heli_Name}>'

class AirGroundMissile(db.Model):
    __tablename__ = 'AirGroundMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Name or 'Unknown Air-Ground Missile'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'Air-to-Ground Missile'

    def __repr__(self):
        return f'<AirGroundMissile {self.Name}>'

class SurfaceMissile(db.Model):
    __tablename__ = 'SurfaceMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Name or 'Unknown Surface Missile'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'Surface Missile'

    def __repr__(self):
        return f'<SurfaceMissile {self.Name}>'

class SeaSurfaceMissile(db.Model):
    __tablename__ = 'SeaSurfaceMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=True)
    Country = db.Column(db.String(50), nullable=True)
    
    @property
    def name(self):
        return self.Name or 'Unknown Sea-Surface Missile'
    
    @property
    def country(self):
        return self.Country or 'Unknown'
    
    @property
    def type(self):
        return 'Sea-to-Surface Missile'

    def __repr__(self):
        return f'<SeaSurfaceMissile {self.Name}>'
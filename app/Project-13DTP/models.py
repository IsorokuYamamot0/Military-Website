from app import db


class MilitaryData(db.Model):
    __tablename__ = 'militarydata'
    VehicleID = db.Column(db.Integer, primary_key=True)
    Country = db.Column(db.String)

class ICBM(db.Model):
    __tablename__ = 'icbm'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class Tanks(db.Model):
    __tablename__ = 'tanks'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class Helicopters(db.Model):
    __tablename__ = 'helicopters'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class Planes(db.Model):
    __tablename__ = 'planes'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class AirGroundMissiles(db.Model):
    __tablename__ = 'airgroundmissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class SurfaceMissiles(db.Model):
    __tablename__ = 'surfacemissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class SeaSurfaceMissiles(db.Model):
    __tablename__ = 'seasurfacemissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))

class Ships(db.Model):
    __tablename__ = 'ships'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))
    Type = db.Column(db.String)

class Submarines(db.Model):
    __tablename__ = 'submarines'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))
    Class = db.Column(db.String)

class Drones(db.Model):
    __tablename__ = 'drones'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))
    Type = db.Column(db.String)

class MissileDefenseSystems(db.Model):
    __tablename__ = 'missiledefensesystems'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))
    Range = db.Column(db.String)

class NavalAircraft(db.Model):
    __tablename__ = 'navalaircraft'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    CountryID = db.Column(db.Integer, db.ForeignKey('militarydata.VehicleID'))
    Role = db.Column(db.String)

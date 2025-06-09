from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Plane(db.Model):
    __tablename__ = 'Planes'
    id_planes = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class Tank(db.Model):
    __tablename__ = 'Tanks'
    id_Tanks = db.Column(db.Integer, primary_key=True)
    Tank_Name = db.Column(db.String, nullable=False)

class ICBM(db.Model):
    __tablename__ = 'ICBM'
    id_ICBM = db.Column(db.Integer, primary_key=True)
    ICBM_Name = db.Column(db.String)

class Helicopter(db.Model):
    __tablename__ = 'Helicopter'
    id_Heli = db.Column(db.Integer, primary_key=True)
    Heli_Name = db.Column(db.String)

class AirGroundMissile(db.Model):
    __tablename__ = 'AirGroundMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class SurfaceMissile(db.Model):
    __tablename__ = 'SurfaceMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

class SeaSurfaceMissile(db.Model):
    __tablename__ = 'SeaSurfaceMissiles'
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)

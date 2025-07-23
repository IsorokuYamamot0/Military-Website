from app import db  # Use db from __init__.py

PizzaTopping = db.Table('PizzaTopping',
    db.Column('pid', db.Integer, db.ForeignKey('Tank.id')),
    db.Column('tid', db.Integer, db.ForeignKey('Plane.id'))  # 'Plane.id' may be a mistake?
)

class Pizza(db.Model):
    __tablename__ = "Tank"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    base_name = db.relationship("Base", backref="pizzas_with_this_base")
    toppings = db.relationship('Topping', secondary=PizzaTopping, back_populates='pizzas')

    def __repr__(self):
        return f"{self.name} Pizza"

class Topping(db.Model):
    __tablename__ = "Topping"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())
    pizzas = db.relationship('Pizza', secondary=PizzaTopping, back_populates='toppings')

class Base(db.Model):
    __tablename__ = "Base"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.Text())

    def __repr__(self):
        return self.name

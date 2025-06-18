# You need a model for each table - this is the 'translation layer'
# between Flask and SQL.  And you need a way to handle the many-to-many
# relationship between Pizza and Topping
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # This should be initialized with your Flask app

# This is a simple many-to-many that just has the two FK's - if you have
# a complex many-to-many that has its own fields (eg: you have a db with
# Actor, Movie and a m2m table called 'Role' that also includes the role
# name and notes) then you'll want to look at my MiniIMDB and/or
# Kiwi Pycon X tutorials
PizzaTopping = db.Table('PizzaTopping',
    db.Column('pid', db.Integer, db.ForeignKey('Pizza.id')),
    db.Column('tid', db.Integer, db.ForeignKey('Topping.id'))
)


class Pizza(db.Model):
  # In Flask-SQLAlchemy __tablename__ is not strictly required if there
  # is an id in the table, because it can figure it out itself...
  # although in vanilla SQLAlchemy it is needed.  It should be set
  # to the name of the table in the database
  __tablename__ = "Pizza"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  description = db.Column(db.Text())
  base = db.Column(db.Integer, db.ForeignKey('Base.id'))
  
  # a one-to-many relationship exists between Base and Pizza
  # one base can be used on many pizzas, but one pizza only has one base
  # so we do the relationship here in Pizza, to the Base class
  base_name = db.relationship("Base", backref="pizzas_with_this_base")
  # Note the odd names - we can't use Pizza.base, as that is already used
  # for the FK, so Pizza.base_name will do - in a many to many it would
  # probably be plural (ie: Pizza.toppings) but there is only one base.

  # Note - the backref saves you writing the same relationship in the other
  # direction in the Topping class - there is also back_populates
  # which you would use if you were also inserting data, but thats for
  # another day...
  # effectively you can now query Pizza, and view all the toppings by
  # looking at pizza.toppings (returns a list of the toppings)
  toppings = db.relationship('Topping', secondary = PizzaTopping, back_populates = 'pizzas')

  def __repr__(self):
    return f'{self.name.upper()} PIZZA' 


class Topping(db.Model):
  __tablename__ = "Topping"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  description = db.Column(db.Text())
  
  pizzas = db.relationship('Pizza', secondary = PizzaTopping, back_populates = 'toppings')


class Base(db.Model):
  __tablename__ = "Base"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String())
  description = db.Column(db.Text())

  def __repr__(self):
    return self.name 
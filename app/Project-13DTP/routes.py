from app import app
from flask import render_template, abort
from flask_sqlalchemy import SQLAlchemy  # no more boring old SQL for us!
import os


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, "pizza.db")
db.init_app(app)
      

import app.models as models


# basic route
@app.route('/')
def root():
    return render_template('home.html', page_title='HOME')


# about route
@app.route('/about')  # note the leading slash, it’s important
def about():
    return render_template('about.html', page_title='ABOUT') 


@app.route('/all_pizzas')
def all_pizzas():
  pizzas = models.Pizza.query.all()
  return render_template("all_pizzas.html", pizzas=pizzas)


# Now lets display one pizza using SQLAlchemy
@app.route('/pizza/<int:id>')
def pizza(id):
    # get the pizza, but throw a 404 if the id doesn't exist
    pizza = models.Pizza.query.filter_by(id=id).first_or_404()
    print(pizza, pizza.toppings)  # DEBUG
    # title = pizza[1].upper() + ' PIZZA' # see Pizza class __repr__
    return render_template('pizza.html', pizza=pizza)


@app.route('/base/<int:id>')
def base(id):
    pizzas = models.Pizza.query.filter_by(base=id).all()
    return render_template("pizzas.html", pizzas=pizzas)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

#if __name__ == "__main__":
#    app.run(debug=True)
from app import app
from flask import render_template
from flask_sqlalchemy import SQLAlchemy  # no more boring old SQL for us!
import os
import app.models as models

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join
(basedir, "USA.db")
db.init_app(app)


# basic route
@app.route('/')
def root():
    return render_template('home.html', page_title='HOME')


# about route
@app.route('/about')  # note the leading slash, it’s important
def about():
    return render_template('about.html', page_title='ABOUT')


# Now lets display one pizza using SQLAlchemy
@app.route('/pizza/<int:id>')
def pizza(id):
    # get the pizza, but throw a 404 if the id doesn't exist
    pizza = models.Pizza.query.filter_by(id=id).first_or_404()
    print(pizza, pizza.toppings)  # DEBUG
    # title = pizza[1].upper() + ' PIZZA' # see Pizza class __repr__
    return render_template('pizza.html', pizza=pizza)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
   app.run(debug=True)

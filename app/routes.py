from app import app
from flask import render_template
from app.models import Pizza


# Root route
@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html', page_title='ABOUT')


@app.route('/pizza/<int:id>')
def pizza(id):
    pizza = Pizza.query.filter_by(id=id).first_or_404()
    print(pizza, pizza.toppings)
    return render_template('pizza.html', pizza=pizza)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

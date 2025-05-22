from flask import Flask, render_template, request
from models import db, Weapon
from app import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///USA.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = Weapon.query.filter(Weapon.name.ilike(f'%{query}%')).all()
    return render_template('search_results.html', query=query, results=results)

@app.route('/country/<name>')
def country(name):
    weapons = Weapon.query.filter_by(country=name).all()
    return render_template('country.html', country=name, weapons=weapons)

from models import Plane, Tank, ICBM, Helicopter, AirGroundMissile

@app.route('/usa/planes')
def usa_planes():
    planes = Plane.query.all()
    return render_template('planes.html', planes=planes)


if __name__ == '__main__':
    app.run(debug=True)

from flask import render_template, request, current_app as app, abort
from .models import (
    Plane, Tank, ICBM, Helicopter, 
    AirGroundMissile, SurfaceMissile, SeaSurfaceMissile
)

# Table configuration
TABLE_MAPPING = {
    'planes': (Plane, 'Aircraft'),
    'tanks': (Tank, 'Ground Vehicles'),
    'icbm': (ICBM, 'Intercontinental Ballistic Missiles'),
    'helicopters': (Helicopter, 'Rotorcraft'),
    'air_ground_missiles': (AirGroundMissile, 'Air-to-Ground Missiles'),
    'surface_missiles': (SurfaceMissile, 'Surface Missiles'),
    'sea_surface_missiles': (SeaSurfaceMissile, 'Sea-to-Surface Missiles')
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


def _query_weapons(country=None, search_term=None):
    """Helper function to query weapons based on country or search term"""
    weapons = []
    models = [model for model, _ in TABLE_MAPPING.values()]
    
    try:
        for model in models:
            query = model.query
            if country:
                query = query.filter(model.Country.ilike(f'%{country}%'))
            elif search_term:
                name_attr = 'Name' if hasattr(model, 'Name') else \
                           'Tank_Name' if hasattr(model, 'Tank_Name') else \
                           'ICBM_Name' if hasattr(model, 'ICBM_Name') else \
                           'Heli_Name'
                query = query.filter(getattr(model, name_attr).ilike(f'%{search_term}%'))
            weapons.extend(query.all())
    except Exception as e:
        app.logger.error(f"Database error: {e}")
    
    return weapons


@app.route('/country/<country_name>')
def country(country_name):
    weapons = _query_weapons(country=country_name)
    return render_template('country.html', country=country_name, weapons=weapons)


@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    weapons = _query_weapons(search_term=query) if query else []
    return render_template('search_results.html', query=query, weapons=weapons)


@app.route('/tables')
def tables():
    tables_info = [(name, display) for name, (_, display) in TABLE_MAPPING.items()]
    return render_template('tables.html', tables=tables_info)


@app.route('/table/<table_name>')
def table_view(table_name):
    if table_name not in TABLE_MAPPING:
        abort(404)
    
    model, _ = TABLE_MAPPING[table_name]
    try:
        rows = model.query.all()
    except Exception as e:
        app.logger.error(f"Table view error: {e}")
        rows = []
    
    return render_template('table.html', 
                         table_name=table_name.replace('_', ' ').title(),
                         display_name=TABLE_MAPPING[table_name][1],
                         rows=rows)
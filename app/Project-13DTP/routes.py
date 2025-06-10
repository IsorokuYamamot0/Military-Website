from flask import render_template, request, current_app as app
from .models import Plane, Tank, ICBM, Helicopter, AirGroundMissile, SurfaceMissile, SeaSurfaceMissile

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/country/<country_name>')
def country(country_name):
    """Display all weapons for a specific country"""
    weapons = []
    
    try:
        # Query each table for weapons from the specified country (case-insensitive)
        planes = Plane.query.filter(Plane.Country.ilike(f'%{country_name}%')).all()
        tanks = Tank.query.filter(Tank.Country.ilike(f'%{country_name}%')).all()
        icbms = ICBM.query.filter(ICBM.Country.ilike(f'%{country_name}%')).all()
        helicopters = Helicopter.query.filter(Helicopter.Country.ilike(f'%{country_name}%')).all()
        ag_missiles = AirGroundMissile.query.filter(AirGroundMissile.Country.ilike(f'%{country_name}%')).all()
        surface_missiles = SurfaceMissile.query.filter(SurfaceMissile.Country.ilike(f'%{country_name}%')).all()
        sea_missiles = SeaSurfaceMissile.query.filter(SeaSurfaceMissile.Country.ilike(f'%{country_name}%')).all()
        
        # Combine all weapons into a single list
        weapons = planes + tanks + icbms + helicopters + ag_missiles + surface_missiles + sea_missiles
        
    except Exception as e:
        app.logger.error(f"Database error in country route: {e}")
        weapons = []
    
    return render_template('country.html', country=country_name, weapons=weapons)

@app.route('/search')
def search():
    """Search for weapons across all tables"""
    query = request.args.get('q', '').strip()
    weapons = []
    
    if query:
        try:
            # Search in each table using the appropriate column names
            planes = Plane.query.filter(Plane.Name.ilike(f'%{query}%')).all()
            tanks = Tank.query.filter(Tank.Tank_Name.ilike(f'%{query}%')).all()
            icbms = ICBM.query.filter(ICBM.ICBM_Name.ilike(f'%{query}%')).all()
            helicopters = Helicopter.query.filter(Helicopter.Heli_Name.ilike(f'%{query}%')).all()
            ag_missiles = AirGroundMissile.query.filter(AirGroundMissile.Name.ilike(f'%{query}%')).all()
            surface_missiles = SurfaceMissile.query.filter(SurfaceMissile.Name.ilike(f'%{query}%')).all()
            sea_missiles = SeaSurfaceMissile.query.filter(SeaSurfaceMissile.Name.ilike(f'%{query}%')).all()
            
            # Combine all search results
            weapons = planes + tanks + icbms + helicopters + ag_missiles + surface_missiles + sea_missiles
            
        except Exception as e:
            app.logger.error(f"Search error: {e}")
            weapons = []
    
    return render_template('search_results.html', query=query, weapons=weapons)

@app.route('/tables')
def tables():
    """Display all available tables"""
    table_names = [
        ('Planes', 'Aircraft'),
        ('Tanks', 'Ground Vehicles'), 
        ('ICBM', 'Intercontinental Ballistic Missiles'),
        ('Helicopter', 'Rotorcraft'),
        ('AirGroundMissiles', 'Air-to-Ground Missiles'),
        ('SurfaceMissiles', 'Surface Missiles'),
        ('SeaSurfaceMissiles', 'Sea-to-Surface Missiles')
    ]
    return render_template('tables.html', tables=table_names)

@app.route('/table/<table_name>')
def table_view(table_name):
    """Display contents of a specific table"""
    rows = []
    
    try:
        if table_name == 'Planes':
            rows = Plane.query.all()
        elif table_name == 'Tanks':
            rows = Tank.query.all()
        elif table_name == 'ICBM':
            rows = ICBM.query.all()
        elif table_name == 'Helicopter':
            rows = Helicopter.query.all()
        elif table_name == 'AirGroundMissiles':
            rows = AirGroundMissile.query.all()
        elif table_name == 'SurfaceMissiles':
            rows = SurfaceMissile.query.all()
        elif table_name == 'SeaSurfaceMissiles':
            rows = SeaSurfaceMissile.query.all()
        else:
            # Handle invalid table name
            return render_template('404.html'), 404
            
    except Exception as e:
        app.logger.error(f"Table view error: {e}")
        rows = []
    
    return render_template('table.html', table_name=table_name, rows=rows)
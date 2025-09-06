# This website is made by Nishil Singh June 1 2025

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from app import app, db
from app.models import Tank, Plane, Country

# Import the new Country model

# --- Application Routes ---

# --- Route for the index/home page ---
# This was taken from last years project. Same with the about page.


@app.route('/')
def homepage():
    """Renders the main home page."""
    return render_template('index.html')

# --- Route for the about page ---


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')

# --- Route for the tank page ---
# This made from ai help and the page.


@app.route('/tanks')
def tanks_list():
    """Renders the page showing all tanks."""
    # Eagerly load countries to avoid N+1 queries in template
    tanks = Tank.query.options(db.joinedload(Tank.countries)).all()
    return render_template('vehicles.html', vehicles=tanks, title="Tanks")

# --- Route for the plane page ---
# This made from ai help and the page.


@app.route('/planes')
def planes_list():
    """Renders the page showing all aircraft."""
    # Eagerly load countries to avoid N+1 queries in template
    planes = Plane.query.options(db.joinedload(Plane.countries)).all()
    return render_template('vehicles.html', vehicles=planes, title="Aircraft")

# --- Route for listing all countries ---

# Also had ai make this route and the page.


@app.route('/countries')
def countries_list():
    """Renders the page showing all countries."""
    countries = Country.query.all()
    return render_template('countries.html', countries=countries)

# --- Route for listing vehicles by a specific country ---

# Had ai fix this route to properly get tanks and planes for a country and help me creat the template and the link on the countries page. Also had ai make this route and the page.


@app.route('/countries/<int:country_id>')
def vehicles_by_country(country_id):
    """Renders the page showing tanks and planes for a specific country."""
    country = Country.query.get_or_404(country_id)
    # Get tanks and planes associated with this country directly
    # country.tanks and country.planes are already lists due to the backref
    tanks = country.tanks  # This is already a list of Tank objects
    planes = country.planes  # This is already a list of Plane objects

    # Combine and sort vehicles if desired, or keep separate
    all_vehicles = sorted(list(tanks) + list(planes), key=lambda v: v.name)

    return render_template('vehicles_by_country.html', country=country, vehicles=all_vehicles)

# --- Route for adding tank ---
# Also had ai make this route and the page.


@app.route('/add_tank', methods=['GET', 'POST'])
def add_tank():
    """Handles adding a new tank to the database."""
    all_countries = Country.query.order_by(Country.name).all()
# Get all countries for the form

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        year_introduced = request.form.get('year_introduced')
        selected_country_ids = request.form.getlist('countries')
# Get list of selected country IDs

        if not name or not description or not year_introduced or not selected_country_ids:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_tank'))

        new_tank = Tank(
            name=name,
            description=description,
            year_introduced=int(year_introduced)
        )
        # Add selected countries to the tank
        for country_id in selected_country_ids:
            country = Country.query.get(country_id)
            if country:
                new_tank.countries.append(country)

        db.session.add(new_tank)
        db.session.commit()
        flash(f'Tank "{name}" added successfully!', 'success')
        return redirect(url_for('tanks_list'))

    return render_template('add_tank.html', title="Add New Tank", all_countries=all_countries)

# --- Route for adding plane ---
# Also had ai make this route and the page.


@app.route('/add_plane', methods=['GET', 'POST'])
def add_plane():
    """Handles adding a new plane to the database."""
    all_countries = Country.query.order_by(Country.name).all()
# Get all countries for the form

    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        description = request.form.get('description')
        selected_country_ids = request.form.getlist('countries')
# Get list of selected country IDs

        if not name or not role or not description or not selected_country_ids:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_plane'))

        new_plane = Plane(
            name=name,
            role=role,
            description=description
        )

        # Add selected countries to the plane
        for country_id in selected_country_ids:
            country = Country.query.get(country_id)
            if country:
                new_plane.countries.append(country)

        db.session.add(new_plane)
        db.session.commit()
        flash(f'Aircraft "{name}" added successfully!', 'success')
        return redirect(url_for('planes_list'))

    return render_template('add_plane.html', title="Add New Aircraft", all_countries=all_countries)


# --- Route for editing an existing tank ---
@app.route('/edit_tank/<int:id>', methods=['GET', 'POST'])
def edit_tank(id):
    """Handles editing a tank's details."""
    tank = Tank.query.options(db.joinedload(Tank.countries)).get_or_404(id)
    all_countries = Country.query.order_by(Country.name).all()
# Get all countries for the form

    if request.method == 'POST':
        tank.name = request.form['name']
        tank.description = request.form['description']
        tank.year_introduced = int(request.form['year_introduced'])
        selected_country_ids = request.form.getlist('countries')

        # Clear existing country associations
        tank.countries.clear()
        # Add new selected country associations
        for country_id in selected_country_ids:
            country = Country.query.get(country_id)
            if country:
                tank.countries.append(country)

        db.session.commit()
        flash(f'Tank "{tank.name}" updated successfully!', 'success')
        return redirect(url_for('tanks_list'))
    return render_template('edit_tank.html', title="Edit Tank", vehicle=tank, all_countries=all_countries)


# --- Route for deleting a tank ---
# Also had ai make this route and the page.

@app.route('/delete_tank/<int:id>', methods=['POST'])
def delete_tank(id):
    """Handles deleting a tank from the database."""
    tank = Tank.query.get_or_404(id)
    db.session.delete(tank)
    db.session.commit()
    flash(f'Tank "{tank.name}" has been deleted.', 'success')
    return redirect(url_for('tanks_list'))


# --- Route for editing an existing plane ---
@app.route('/edit_plane/<int:id>', methods=['GET', 'POST'])
def edit_plane(id):
    """Handles editing a plane's details."""
    plane = Plane.query.options(db.joinedload(Plane.countries)).get_or_404(id)
    all_countries = Country.query.order_by(Country.name).all()
# Get all countries for the form

    if request.method == 'POST':
        plane.name = request.form['name']
        plane.role = request.form['role']
        plane.description = request.form['description']
        selected_country_ids = request.form.getlist('countries')

        # Clear existing country associations
        plane.countries.clear()
        # Add new selected country associations
        for country_id in selected_country_ids:
            country = Country.query.get(country_id)
            if country:
                plane.countries.append(country)

        db.session.commit()
        flash(f'Aircraft "{plane.name}" updated successfully!', 'success')
        return redirect(url_for('planes_list'))
    return render_template('edit_plane.html', title="Edit Aircraft", vehicle=plane, all_countries=all_countries)

# --- Route for deleting a plane ---
# Also had ai make this route and the page.


@app.route('/delete_plane/<int:id>', methods=['POST'])
def delete_plane(id):
    """Handles deleting a plane from the database."""
    plane = Plane.query.get_or_404(id)
    db.session.delete(plane)
    db.session.commit()
    flash(f'Aircraft "{plane.name}" has been deleted.', 'success')
    return redirect(url_for('planes_list'))

# --- Route for searching vehicles ---
# This tooke time for me to figure out. Had ai help me with this route and the page.


@app.route('/search')
def search():
    """Handles searching for tanks and planes by name or description."""
    query = request.args.get('q', '').strip()
    results = []

    if query:
        # Search for tanks
        tanks = Tank.query.options(db.joinedload(Tank.countries)).filter(
            or_(
                Tank.name.ilike(f'%{query}%'),
                Tank.description.ilike(f'%{query}%')
            )
        ).all()
        for tank in tanks:
            tank.type = 'Tank'  # Add type for display
            results.append(tank)

        # Search for planes
        planes = Plane.query.options(db.joinedload(Plane.countries)).filter(
            or_(
                Plane.name.ilike(f'%{query}%'),
                Plane.description.ilike(f'%{query}%'),
                Plane.role.ilike(f'%{query}%')
            )
        ).all()
        for plane in planes:
            plane.type = 'Aircraft'  # Add type for display
            results.append(plane)

    # Sort results by name for consistent display
    results.sort(key=lambda x: x.name)
    return render_template('search_results.html', vehicles=results, query=query)

# --- Error Handlers ---
# These two error handlers were added by me from last years project adn will trigger when a 404 or 500 error occurs.


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

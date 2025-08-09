# This website is made by Nishil Singh June 1 2025

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from app import app, db
from app.models import Tank, Plane

# --- Application Routes ---


@app.route('/')
def homepage():
    """Renders the main home page."""
    return render_template('index.html')


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html')


@app.route('/tanks')
def tanks_list():
    """Renders the page showing all tanks."""
    tanks = Tank.query.all()
    return render_template('vehicles.html', vehicles=tanks, title="USA Tanks")


@app.route('/planes')
def planes_list():
    """Renders the page showing all aircraft."""
    planes = Plane.query.all()
    return render_template('vehicles.html', vehicles=planes, title="USA Aircraft")


@app.route('/add_tank', methods=['GET', 'POST'])
def add_tank():
    """Handles adding a new tank to the database."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        year_introduced = request.form.get('year_introduced')

        if not name or not description or not year_introduced:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_tank'))

        new_tank = Tank(
            name=name,
            description=description,
            year_introduced=int(year_introduced)
        )
        db.session.add(new_tank)
        db.session.commit()
        flash(f'Tank "{name}" added successfully!', 'success')
        return redirect(url_for('tanks_list'))

    return render_template('add_tank.html', title="Add New Tank")


@app.route('/add_plane', methods=['GET', 'POST'])
def add_plane():
    """Handles adding a new plane to the database."""
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        description = request.form.get('description')

        if not name or not role or not description:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_plane'))

        new_plane = Plane(
            name=name,
            role=role,
            description=description
        )
        db.session.add(new_plane)
        db.session.commit()
        flash(f'Aircraft "{name}" added successfully!', 'success')
        return redirect(url_for('planes_list'))

    return render_template('add_plane.html', title="Add New Aircraft")


# --- Route for editing an existing tank ---
@app.route('/edit_tank/<int:id>', methods=['GET', 'POST'])
def edit_tank(id):
    """Handles editing a tank's details."""
    tank = Tank.query.get_or_404(id)
    if request.method == 'POST':
        tank.name = request.form['name']
        tank.description = request.form['description']
        tank.year_introduced = int(request.form['year_introduced'])
        db.session.commit()
        flash(f'Tank "{tank.name}" updated successfully!', 'success')
        return redirect(url_for('tanks_list'))
    return render_template('edit_tank.html', title="Edit Tank", vehicle=tank)


# --- Route for deleting a tank ---
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
    plane = Plane.query.get_or_404(id)
    if request.method == 'POST':
        plane.name = request.form['name']
        plane.role = request.form['role']
        plane.description = request.form['description']
        db.session.commit()
        flash(f'Aircraft "{plane.name}" updated successfully!', 'success')
        return redirect(url_for('planes_list'))
    return render_template('edit_plane.html', title="Edit Aircraft", vehicle=plane)


# --- Route for deleting a plane ---
@app.route('/delete_plane/<int:id>', methods=['POST'])
def delete_plane(id):
    """Handles deleting a plane from the database."""
    plane = Plane.query.get_or_404(id)
    db.session.delete(plane)
    db.session.commit()
    flash(f'Aircraft "{plane.name}" has been deleted.', 'success')
    return redirect(url_for('planes_list'))


@app.route('/search')
def search():
    """Handles search queries and displays results."""
    query = request.args.get('q', '')
    if not query:
        return render_template('search_results.html', query=query, vehicles=[])

    search_term = f"%{query}%"
    tanks = Tank.query.filter(or_(Tank.name.ilike(search_term), Tank.description.ilike(search_term))).all()
    planes = Plane.query.filter(or_(Plane.name.ilike(search_term), Plane.description.ilike(search_term), Plane.role.ilike(search_term))).all()
    results = tanks + planes
    return render_template('search_results.html', query=query, vehicles=results)


# --- Error Handlers ---

@app.errorhandler(404)
def page_not_found(e):
    """Renders the 404 error page."""
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Renders the 500 error page for server errors."""
    return render_template("500.html"), 500

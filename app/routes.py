# This website is made by Nishil Singh June 1 2025

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import or_
from app import app, db, login_manager # Import login_manager
from app.models import Tank, Plane, Country, User # Import User
from flask_login import login_user, logout_user, login_required, current_user # Import Flask-Login functions
from functools import wraps # Import wraps for custom decorators

# --- Custom Decorator for Admin Only Access ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('homepage')) # Or redirect to login, or 403 page
        return f(*args, **kwargs)
    return decorated_function

# --- User Loader for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Authentication Routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form_data = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not username or not password or not password_confirm:
            flash('All fields are required!', 'error')
            form_data = request.form
        elif password != password_confirm:
            flash('Passwords do not match!', 'error')
            form_data = request.form
        elif User.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            form_data = request.form
        else:
            # First registered user becomes admin by default for easy setup
            # In a real app, this would be managed through a separate admin panel or initial script
            is_admin_user = (User.query.count() == 0)
            user = User(username=username, is_admin=is_admin_user)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            if is_admin_user:
                flash('Registration successful! You are the administrator. Please log in.', 'success')
            else:
                flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form_data=form_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form_data = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required!', 'error')
            form_data = request.form
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash(f'Logged in successfully! {"(Administrator)" if user.is_admin else ""}', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('homepage'))
            else:
                flash('Invalid username or password', 'error')
                form_data = request.form
    return render_template('login.html', title='Login', form_data=form_data)


@app.route('/logout')
@login_required # Only logged-in users can log out
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('homepage'))


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
@admin_required
def add_tank():
    """Handles adding a new tank to the database."""
    all_countries = Country.query.order_by(Country.name).all()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        year_introduced = request.form.get('year_introduced')
        external_link = request.form.get('external_link') # Get the new field
        selected_country_ids = request.form.getlist('countries')

        if not name or not description or not year_introduced or not selected_country_ids:
            flash('All required fields are missing!', 'error')
            return redirect(url_for('add_tank'))

        new_tank = Tank(
            name=name,
            description=description,
            year_introduced=int(year_introduced),
            external_link=external_link if external_link else None # Store the link, or None if empty
        )
        for country_id in selected_country_ids:
            country = Country.query.get(country_id)
            if country:
                new_tank.countries.append(country)

        db.session.add(new_tank)
        db.session.commit()
        flash(f'Tank "{name}" added successfully!', 'success')
        return redirect(url_for('tanks_list'))

    return render_template('add_tank.html', title="Add New Tank", all_countries=all_countries)


@app.route('/add_plane', methods=['GET', 'POST'])
@admin_required
def add_plane():
    """Handles adding a new plane to the database."""
    all_countries = Country.query.order_by(Country.name).all()

    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        description = request.form.get('description')
        external_link = request.form.get('external_link') # Get the new field
        selected_country_ids = request.form.getlist('countries')

        if not name or not role or not description or not selected_country_ids:
            flash('All required fields are missing!', 'error')
            return redirect(url_for('add_plane'))

        new_plane = Plane(
            name=name,
            role=role,
            description=description,
            external_link=external_link if external_link else None # Store the link, or None if empty
        )
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
@admin_required
def edit_tank(id):
    """Handles editing a tank's details."""
    tank = Tank.query.options(db.joinedload(Tank.countries)).get_or_404(id)
    all_countries = Country.query.order_by(Country.name).all()

    if request.method == 'POST':
        tank.name = request.form['name']
        tank.description = request.form['description']
        tank.year_introduced = int(request.form['year_introduced'])
        tank.external_link = request.form.get('external_link') # Update the new field
        selected_country_ids = request.form.getlist('countries')

        tank.countries.clear()
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
@admin_required # Protect this route with admin decorator
def delete_tank(id):
    """Handles deleting a tank from the database."""
    tank = Tank.query.get_or_404(id)
    db.session.delete(tank)
    db.session.commit()
    flash(f'Tank "{tank.name}" has been deleted.', 'success')
    return redirect(url_for('tanks_list'))


# --- Route for editing an existing plane ---
@app.route('/edit_plane/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_plane(id):
    """Handles editing a plane's details."""
    plane = Plane.query.options(db.joinedload(Plane.countries)).get_or_404(id)
    all_countries = Country.query.order_by(Country.name).all()

    if request.method == 'POST':
        plane.name = request.form['name']
        plane.role = request.form['role']
        plane.description = request.form['description']
        plane.external_link = request.form.get('external_link') # Update the new field
        selected_country_ids = request.form.getlist('countries')

        plane.countries.clear()
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
@admin_required # Protect this route with admin decorator
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


# --- New Routes for Favoriting Vehicles ---
@app.route('/favorite_tank/<int:tank_id>', methods=['POST'])
@login_required
def favorite_tank(tank_id):
    tank = Tank.query.get_or_404(tank_id)
    if tank not in current_user.favorite_tanks:
        current_user.favorite_tanks.append(tank)
        db.session.commit()
        flash(f'"{tank.name}" added to your favorites!', 'success')
    else:
        flash(f'"{tank.name}" is already in your favorites.', 'info')
    return redirect(request.referrer or url_for('tanks_list')) # Redirect back to the previous page

@app.route('/unfavorite_tank/<int:tank_id>', methods=['POST'])
@login_required
def unfavorite_tank(tank_id):
    tank = Tank.query.get_or_404(tank_id)
    if tank in current_user.favorite_tanks:
        current_user.favorite_tanks.remove(tank)
        db.session.commit()
        flash(f'"{tank.name}" removed from your favorites.', 'info')
    else:
        flash(f'"{tank.name}" was not in your favorites.', 'error')
    return redirect(request.referrer or url_for('tanks_list')) # Redirect back to the previous page

@app.route('/favorite_plane/<int:plane_id>', methods=['POST'])
@login_required
def favorite_plane(plane_id):
    plane = Plane.query.get_or_404(plane_id)
    if plane not in current_user.favorite_planes:
        current_user.favorite_planes.append(plane)
        db.session.commit()
        flash(f'"{plane.name}" added to your favorites!', 'success')
    else:
        flash(f'"{plane.name}" is already in your favorites.', 'info')
    return redirect(request.referrer or url_for('planes_list')) # Redirect back to the previous page

@app.route('/unfavorite_plane/<int:plane_id>', methods=['POST'])
@login_required
def unfavorite_plane(plane_id):
    plane = Plane.query.get_or_404(plane_id)
    if plane in current_user.favorite_planes:
        current_user.favorite_planes.remove(plane)
        db.session.commit()
        flash(f'"{plane.name}" removed from your favorites.', 'info')
    else:
        flash(f'"{plane.name}" was not in your favorites.', 'error')
    return redirect(request.referrer or url_for('planes_list')) # Redirect back to the previous page

@app.route('/favorites')
@login_required
def favorites():
    """Renders the page showing a user's favorited vehicles."""
    # Eagerly load related data for favorited vehicles
    user_with_favorites = User.query.options(
        db.joinedload(User.favorite_tanks).joinedload(Tank.countries),
        db.joinedload(User.favorite_planes).joinedload(Plane.countries)
    ).get(current_user.id)

    favorited_tanks = user_with_favorites.favorite_tanks
    favorited_planes = user_with_favorites.favorite_planes

    all_favorited_vehicles = sorted(
        list(favorited_tanks) + list(favorited_planes),
        key=lambda v: v.name
    )
    return render_template('favorites.html', vehicles=all_favorited_vehicles, title="My Favorites")

# --- New Route for adding countries ---
@app.route('/add_country', methods=['GET', 'POST'])
@admin_required # Protect this route with admin decorator
def add_country():
    """Handles adding a new country to the database."""
    if request.method == 'POST':
        name = request.form.get('name').strip()
        if not name:
            flash('Country name is required!', 'error')
        elif Country.query.filter_by(name=name).first():
            flash(f'Country "{name}" already exists!', 'error')
        else:
            new_country = Country(name=name)
            db.session.add(new_country)
            db.session.commit()
            flash(f'Country "{name}" added successfully!', 'success')
            return redirect(url_for('countries_list'))
    return render_template('add_country.html', title="Add New Country")


# --- Error Handlers ---
# These two error handlers were added by me from last years project adn will trigger when a 404 or 500 error occurs.


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

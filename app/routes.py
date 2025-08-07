from flask import render_template, request
from sqlalchemy import or_
from app import app
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

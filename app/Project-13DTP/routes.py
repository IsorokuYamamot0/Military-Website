from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import app.models as models


# Route for the about page
@app.route("/about")
def about():
    return render_template("about.html", title="About Page") # Render the about.html template with a title


# Route for the index page
@app.route("/index")
def index():
    return render_template("index.html", title="index Page") # Render the index.html template with a title

# Route for the home page
@app.route("/home")
def home():
    return render_template("home.html", title="home Page") # Render the home.html template with a title

# Route for the info page displaying top ten hypercars
@app.route("/info")
def funfactspg():
    return render_template("info.html", title="Top Ten Hypercars")# Render the info.html template with a title

# Custom 404 error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404_error.html'), 404

# Custom 500 error handler
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500_error.html'), 500


# Run the Flask application in debug mode if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
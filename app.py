from flask import Flask, render_template, request
from  models import db
from app import app



if __name__ == '__main__':
    app.run(debug=True)

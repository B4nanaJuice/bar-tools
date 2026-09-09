from flask import Blueprint, render_template, url_for

from app.database import db
from app.models import Cocktail

page = Blueprint("home", __name__)

@page.route("/")
def index():

    page = db.paginate(db.select(Cocktail).order_by(Cocktail.name))
    
    return render_template("home.html", pagination = page)
from flask import Blueprint, render_template, url_for, request

from app.database import db
from app.models import Cocktail, Tag, Ingredient

page = Blueprint("home", __name__)

@page.route("/")
def index():

    page = db.paginate(db.select(Cocktail).order_by(Cocktail.name))
    tags = Tag.query.all()
    ingredients = Ingredient.query.all()
    
    return render_template("home.html", pagination = page, tags = tags, ingredients = ingredients)
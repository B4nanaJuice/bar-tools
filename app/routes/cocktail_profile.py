from flask import Blueprint, render_template

from app.database import db
from app.models import Cocktail

page = Blueprint("cocktail_profile", __name__)

@page.route("/cocktail/<string:cocktail_name>")
def cocktail_profile(cocktail_name: str):

    cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.name == cocktail_name))
    
    return f"{cocktail.name}"
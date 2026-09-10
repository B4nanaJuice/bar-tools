from flask import Blueprint, render_template

from app.database import db
from app.models import Cocktail

page = Blueprint("cocktail_profile", __name__)

@page.route("/cocktail/<int:cocktail_id>")
def cocktail_profile(cocktail_id: int):

    cocktail = db.get_or_404(Cocktail, cocktail_id)
    
    return f"{cocktail.name}"
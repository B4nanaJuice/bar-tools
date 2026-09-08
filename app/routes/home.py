from flask import Blueprint

from app.services.cocktail_service import CocktailService

page = Blueprint("home", __name__)

@page.route("/")
def index():
    return CocktailService.get_cocktails()
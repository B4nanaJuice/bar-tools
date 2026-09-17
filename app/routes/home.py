from flask import Blueprint, render_template, url_for, request
from sqlalchemy import func

from app.database import db
from app.models import Cocktail, Tag, Ingredient, CocktailIngredient, CocktailTag

page = Blueprint("home", __name__)

@page.route("/")
def index():

    base_query = db.select(Cocktail)

    # Get URL arguments
    ingredients = request.args.get("ingredients")
    if ingredients is not None:
        ingredients = [int(_) for _ in ingredients.split(',')]
        base_query = base_query.join(Cocktail.ingredient_associations) \
                               .where(CocktailIngredient.ingredient_id.in_(ingredients)) \
                               .group_by(Cocktail.id) \
                               .order_by(func.count(CocktailIngredient.ingredient_id).desc())

    tags = request.args.get("tags")
    if tags is not None:
        tags = [int(_) for _ in tags.split(',')]
        base_query = base_query.join(Cocktail.tag_associations) \
                               .where(CocktailTag.tag_id.in_(tags))

    name = request.args.get("name")
    if name is not None:
        base_query = base_query.where(Cocktail.name.ilike(f'%{name.lower()}%'))

    page = db.paginate(base_query, per_page = 12)
    tags = Tag.query.all()
    ingredients = Ingredient.query.all()

    endpoint_args = request.args.to_dict()
    if "page" in endpoint_args:
        del endpoint_args["page"]
    
    return render_template("home.html.jinja", pagination = page, tags = tags, ingredients = ingredients, endpoint = request.endpoint, args = endpoint_args)
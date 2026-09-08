from flask import Flask

from app.cli import seed
from app.database import init_db

def create_app():
    app = Flask(__name__)
    init_db(app = app)

    from app.routes import home_page
    from app.models import CocktailIngredient, CocktailTag, Cocktail, Ingredient, OrderItem, Order, Tag

    # Blueprints
    app.register_blueprint(home_page)

    # CLI Commands
    app.cli.add_command(seed)

    return app
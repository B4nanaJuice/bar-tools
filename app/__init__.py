from flask import Flask, render_template

from app.cli import seed
from app.database import init_db

def create_app():
    app = Flask(__name__)
    init_db(app = app)

    from app.routes import home_page, cocktail_profile
    from app.models import CocktailIngredient, CocktailTag, Cocktail, Ingredient, OrderItem, Order, Tag

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Blueprints
    app.register_blueprint(home_page)
    app.register_blueprint(cocktail_profile)

    # CLI Commands
    app.cli.add_command(seed)

    return app
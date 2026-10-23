from flask import Flask, render_template, abort
import os

from app.cli import seed
from app.database import init_db

def create_app():
    app = Flask(__name__)
    init_db(app = app)

    app.secret_key = os.environ["APP_SECRET"]

    from app.routes import home_page, api, admin, auth
    from app.models import CocktailIngredient, CocktailTag, Cocktail, Ingredient, OrderItem, Order, OrderStatus, Tag

    @app.errorhandler(401)
    def page_unauthorize(e):
        return render_template('errors/401.html.jinja'), 401
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html.jinja'), 404

    @app.errorhandler(418)
    def page_teapot(e):
        return render_template('errors/418.html.jinja'), 418
    @app.get('/teapot')
    def teapot():
        abort(418)

    @app.errorhandler(429)
    def page_too_many_requests(e):
        return render_template('errors/429.html.jinja'), 429

    # Blueprints
    app.register_blueprint(home_page)
    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(admin)

    # CLI Commands
    app.cli.add_command(seed)

    return app
import click
from flask import current_app
from flask.cli import with_appcontext

from app.database import db
from app.models import Cocktail, CocktailIngredient, CocktailTag
from app.models import Ingredient, Tag

@click.command("seed")
@with_appcontext
def seed():
    
    click.echo("This is the start of the seeding process...")

    click.echo("End of the process !")

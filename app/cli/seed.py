import click
from flask import current_app
from flask.cli import with_appcontext
import json

from app.database import db
from app.models import Cocktail, CocktailIngredient, CocktailTag
from app.models import Ingredient, Tag

@click.command("seed")
@with_appcontext
def seed():

    with open("app/cli/seed_data.json", mode = "r", encoding = "utf-8") as f:
        data = json.load(fp = f)["cocktails"]

        click.echo(f"Loading {len(data)} cocktails")

    click.echo("End of the process !")

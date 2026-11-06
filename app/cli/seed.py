import click
from flask import current_app
from flask.cli import with_appcontext
import json

from app.database import db
from app.models import Cocktail, CocktailIngredient, CocktailTag
from app.models import Ingredient, Tag, IngredientCategory
from app.models import OrderStatus, Glass

@click.command("seed")
@click.argument("filename")
@with_appcontext
def seed(filename: str):

    # Add order status
    states = ["new", "pending", "finished"]
    for state_name in states:
        order_status = db.session.scalar(
            db.select(OrderStatus).where(OrderStatus.state == state_name)
        )

        if order_status is None:
            db.session.add(OrderStatus(state = state_name))

    # Add ingredient categories
    ingredient_categories_data = ["spirit", "liquor", "juice", "syrup", "other"]
    ingredient_categories = {}
    for category_name in ingredient_categories_data:
        ingredient_category = db.session.scalar(
            db.select(IngredientCategory).where(IngredientCategory.name == category_name)
        )

        if ingredient_category is None:
            ingredient_category = IngredientCategory(
                name = category_name
            )
            db.session.add(ingredient_category)

        ingredient_categories[category_name] = ingredient_category

    db.session.flush()

    with open(f"app/cli/{filename}", mode = "r", encoding = "utf-8") as f:
        data = json.load(fp = f)["cocktails"]

        click.echo(f"Loaded {len(data)} cocktails")

    # LOADING CONFIG
    with open(f"app/cli/config.json", mode = "r", encoding = "utf-8") as f:
        config_data = json.load(fp = f)
        config_ingredients = config_data["ingredients"]
        config_tags = config_data["tags"]

        click.echo(f"Loading config for {len(config_ingredients.keys())} ingredient{"s" if len(config_ingredients.keys()) != 1 else ""} and {len(config_tags.keys())} tag{"s" if len(config_tags.keys()) != 1 else ""}.")

    # Ingredients
    ingredients_data = [[ing[0] for ing in cocktail["ingredients"]] for cocktail in data]
    from itertools import chain
    ingredients_data = list(set(chain.from_iterable(ingredients_data)))
    ingredients = {}

    for name in ingredients_data:
        ingredient = db.session.scalar(
            db.select(Ingredient).where(Ingredient.name == name)
        )

        if ingredient is None:
            ingredient = Ingredient(
                name = name,
                color = (config_ingredients.get(name) or {}).get("color") or "ffffff",
                category = ingredient_categories.get((config_ingredients.get(name) or {}).get("category")) or ingredient_categories["other"]
            )
            db.session.add(ingredient)

        ingredients[name] = ingredient

    # Tags
    tags_data = [cocktail["tags"] for cocktail in data]
    tags_data = list(set(chain.from_iterable(tags_data)))
    tags = {}

    for name in tags_data:
        tag = db.session.scalar(
            db.select(Tag).where(Tag.name == name)
        )

        if tag is None:
            tag = Tag(
                name = name,
                color = (config_tags.get(name) or {}).get("color") or "ffffff"
            )
            db.session.add(tag)

        tags[name] = tag

    # Verres
    glass_data = [cocktail["glass"] for cocktail in data]
    glass_data = list(set(glass_data))
    glasses = {}

    for name in glass_data:
        glass = db.session.scalar(
            db.select(Glass).where(Glass.name == name)
        )

        if glass is None:
            glass = Glass(name = name)
            db.session.add(glass)

        glasses[name] = glass

    db.session.flush()

    # Cocktails
    for cocktail_data in data:
        cocktail = db.session.scalar(
            db.select(Cocktail).where(Cocktail.name == cocktail_data["name"])
        )

        if cocktail is None:
            cocktail = Cocktail(
                name = cocktail_data["name"],
                description = cocktail_data["description"],
                glass = glasses[cocktail_data["glass"]]
            )

            db.session.add(cocktail)
            db.session.flush()
        else:
            continue

        for ingredient_name, quantity, unit in cocktail_data["ingredients"]:
            ingredient = ingredients[ingredient_name]

            association = db.session.scalar(
                db.select(CocktailIngredient).where(
                    CocktailIngredient.cocktail_id == cocktail.id,
                    CocktailIngredient.ingredient_id == ingredient.id
                )
            )

            if association is None:
                db.session.add(
                    CocktailIngredient(
                        cocktail = cocktail,
                        ingredient = ingredient,
                        quantity = quantity,
                        unit = unit
                    )
                )

        for tag_name in cocktail_data["tags"]:
            tag = tags[tag_name]

            association = db.session.scalar(
                db.select(CocktailTag).where(
                    CocktailTag.cocktail_id == cocktail.id,
                    CocktailTag.tag_id == tag.id
                )
            )

            if association is None:
                db.session.add(
                    CocktailTag(
                        cocktail = cocktail,
                        tag = tag
                    )
                )

    db.session.commit()

    click.echo("End of the process !")

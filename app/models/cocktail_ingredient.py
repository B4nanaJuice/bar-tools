from app.database import db

class CocktailIngredient(db.Model):
    __tablename__: str = "cocktail_ingredients"

    id = db.Column(db.Integer, primary_key = True)

    quantity = db.Column(db.Numeric(10, 2), nullable = False)
    unit = db.Column(db.String(30), nullable = False)

    cocktail_id = db.Column(db.Integer, db.ForeignKey("cocktails.id"), nullable = False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable = False)

    cocktail = db.relationship("Cocktail", back_populates = "ingredient_associations")
    ingredient = db.relationship("Ingredient", back_populates = "cocktail_associations")
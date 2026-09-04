from app import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False, unique = True)

    cocktail_associations = db.relationship("CocktailIngredient", back_populates = "ingredient", cascade = "all, delete-orphan")

    def __repr__(self):
        return f"<Ingredient {self.name}>"
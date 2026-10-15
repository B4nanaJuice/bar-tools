from app.database import db

class IngredientCategory(db.Model):
    __tablename__ = "ingredient_categories"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(32), nullable = False, unique = True)

    ingredients = db.relationship("Ingredient", back_populates = "category")

    def __repr__(self):
        return f"<IngredientCategory {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
from app.database import db

class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(100), nullable = False, unique = True)
    is_available = db.Column(db.Boolean, nullable = False, default = False, server_default = db.text('false'))
    color = db.Column(db.String(16), nullable = False, default = "123456", server_default = db.text("123456"))

    cocktail_associations = db.relationship("CocktailIngredient", back_populates = "ingredient", cascade = "all, delete-orphan")

    def __repr__(self):
        return f"<Ingredient {self.name}>"
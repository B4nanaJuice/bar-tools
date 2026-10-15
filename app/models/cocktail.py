from app.database import db

class Cocktail(db.Model):
    __tablename__ = "cocktails"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(150), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = True)
    image_url = db.Column(db.String(500), nullable = True)

    ingredient_associations = db.relationship("CocktailIngredient", back_populates = "cocktail", cascade = "all, delete-orphan")
    tag_associations = db.relationship("CocktailTag", back_populates = "cocktail", cascade = "all, delete-orphan")
    order_items = db.relationship("OrderItem", back_populates = "cocktail")

    glass_id = db.Column(db.Integer, db.ForeignKey("glass.id"), nullable = False)
    glass = db.relationship("Glass", back_populates = "cocktails")

    def __repr__(self):
        return f"<Cocktail {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "glass": self.glass.to_dict(),

            "ingredients": [_.to_dict() for _ in self.ingredient_associations],
            "tags": [_.to_dict() for _ in self.tag_associations]
        }
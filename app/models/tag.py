from app import db


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(50), nullable = False, unique = True)

    cocktail_associations = db.relationship("CocktailTag", back_populates = "tag", cascade = "all, delete-orphan")

    def __repr__(self):
        return f"<Tag {self.name}>"
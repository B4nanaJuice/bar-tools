from app.database import db

class CocktailTag(db.Model):
    __tablename__ = "cocktail_tags"

    id = db.Column(db.Integer, primary_key = True)

    cocktail_id = db.Column(db.Integer, db.ForeignKey("cocktails.id"), nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), nullable = False)
    
    cocktail = db.relationship("Cocktail", back_populates = "tag_associations")
    tag = db.relationship("Tag", back_populates = "cocktail_associations")

    __table_args__ = (
        db.UniqueConstraint(
            "cocktail_id",
            "tag_id",
            name="uq_cocktail_tag"
        ),
    )
from app.database import db

class Glass(db.Model):
    __tablename__ = "glass"

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(32), nullable = False, unique = True)

    cocktails = db.relationship("Cocktail", back_populates = "glass")

    def __repr__(self):
        return f"<Glass {self.name}>"
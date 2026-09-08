from app.database import db

from app.models import Cocktail

class CocktailService:

    @staticmethod
    def get_cocktails():
        return db.session.execute(db.select(Cocktail)).first().name
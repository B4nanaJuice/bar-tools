from app import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key = True)

    quantity = db.Column(db.Integer, nullable = False, default = 1)

    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable = False)
    cocktail_id = db.Column(db.Integer, db.ForeignKey("cocktails.id"), nullable = False)

    order = db.relationship("Order", back_populates = "items")
    cocktail = db.relationship("Cocktail", back_populates = "order_items")
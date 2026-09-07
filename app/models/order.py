from datetime import datetime, timezone

from app.database import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)

    customer_name = db.Column(db.String(100), nullable = False)
    status = db.Column(db.String(20), nullable = False, default = "pending")
    created_at = db.Column(db.DateTime(timezone = True), nullable = False, default = lambda: datetime.now(timezone.utc))
    validated_at = db.Column(db.DateTime(timezone = True), nullable = True)

    items = db.relationship("OrderItem", back_populates = "order", cascade = "all, delete-orphan")

    def __repr__(self):
        return f"<Order {self.id} - {self.customer_name}>"
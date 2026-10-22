from datetime import datetime, timezone

from app.database import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key = True)

    customer_name = db.Column(db.String(100), nullable = False)
    created_at = db.Column(db.DateTime(timezone = True), nullable = False, default = lambda: datetime.now(timezone.utc))

    items = db.relationship("OrderItem", back_populates = "order", cascade = "all, delete-orphan")

    status_id = db.Column(db.Integer, db.ForeignKey("order_status.id"), nullable = False, default = 0, server_default = db.text('0'))
    status = db.relationship("OrderStatus", back_populates = "orders")

    def __repr__(self):
        return f"<Order {self.id} - {self.customer_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "created_at": self.created_at,
            "items": [_.to_dict() for _ in self.items],
            "status": self.status.to_dict()
        }
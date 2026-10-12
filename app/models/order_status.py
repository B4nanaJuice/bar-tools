from app.database import db

class OrderStatus(db.Model):
    __tablename__ = "order_status"

    # 0: new
    # 1: pending
    # 2: finished

    id = db.Column(db.Integer, primary_key = True)

    state = db.Column(db.String(20), nullable = False, unique = True)

    orders = db.relationship("Order", back_populates = "status")

    def __repr__(self):
        return f"<OrderStatus {self.state}>"
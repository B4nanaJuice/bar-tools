from flask import Blueprint, render_template, url_for, request, jsonify

from app.database import db
from app.models import Cocktail, Tag, Ingredient, Order, OrderItem

page = Blueprint("api", __name__, url_prefix = '/api')

@page.post("/send-order")
def send_order():

    data = request.json
    customer_name: str = data["name"]

    order = Order(customer_name = customer_name)
    db.session.add(order)
    db.session.flush()
    del data["name"]

    for cocktail_id in data:

        cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == int(cocktail_id)))
        if cocktail is None:
            return jsonify({"message": "Cocktail Invalide"}), 400

        db.session.add(
            OrderItem(
                order = order,
                cocktail = cocktail,
                quantity = int(data[cocktail_id])
            )
        )

    db.session.commit()

    return jsonify({"message": "Commande passée !", "orderId": order.id}), 200
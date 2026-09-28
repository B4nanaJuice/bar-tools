from flask import Blueprint, render_template, url_for, request, jsonify
import re

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

        try:
            assert re.match(r'^[0-9]+$', cocktail_id), "Le cocktail demandé est invalide. Vérifie ton panier avant de recommencer."
            cocktail_id = int(cocktail_id)
            assert cocktail_id > 0, "Le cocktail demandé est invalide. Vérifie ton panier avant de recommencer."

            cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == cocktail_id))

            if cocktail is None:
                return jsonify({"message": "Le cocktail demandé est invalide. Vérifie ton panier avant de recommencer."}), 400

            db.session.add(
                OrderItem(
                    order = order,
                    cocktail = cocktail,
                    quantity = int(data[cocktail_id])
                )
            )

        except Exception as e:
            return jsonify({"message": e}), 400

    db.session.commit()

    return jsonify({"message": "Ta commande a bien été passée ! Tu recevras bientôt ce que tu as demandé.", "orderId": order.id}), 200
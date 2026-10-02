from flask import Blueprint, url_for, request, jsonify, session
import os 
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
                    quantity = int(data[f"{cocktail_id}"])
                )
            )

        except Exception as e:
            return jsonify({"message": e}), 400

    db.session.commit()

    return jsonify({"message": "Ta commande a bien été passée ! Tu recevras bientôt ce que tu as demandé.", "orderId": order.id}), 200

@page.get('/get-order-status')
def get_order_status():

    try:
        order_id = request.args.get("order-id")
        order_id = int(order_id)

        order = db.session.scalar(db.select(Order).where(Order.id == order_id))

        if order is None:
            return jsonify({"status": None})

        return jsonify({"status": order.status})
    except:
        return jsonify({"status": None})

@page.post('/update-order-status')
def update_order_stats() :

    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return jsonify({"message": "Tu dois être connecté pour accéder à cette fonctionnalité."}), 401

    data = request.json
    order_id = data['order_id']
    order = db.session.scalar(db.select(Order).where(Order.id == order_id))

    if order is None:
        return jsonify({"message": "Aucune commande n'existe avec cet ID."}), 400

    try:
        order.status = data["status"]
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "Le statut de la commande a bien été changé.", "status": data["status"]}), 200
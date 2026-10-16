from flask import Blueprint, url_for, request, jsonify, session
import os 
import re

from app.database import db
from app.models import Cocktail, Tag, Ingredient, Order, OrderItem, OrderStatus, IngredientCategory

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
            return jsonify({"status": None}), 400

        return jsonify({"status": order.status.state}), 200
    except:
        return jsonify({"status": None}), 400

@page.get('/get-cocktail')
def get_cocktail():

    try:
        cocktail_id = request.args.get("cocktail-id")
        cocktail_id = int(cocktail_id)

        cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == cocktail_id))

        if cocktail is None:
            return jsonify({"cocktail": None}), 400

        return jsonify({"cocktail": cocktail.to_dict()}), 200
    except:
        return jsonify({"cocktail": None}), 400

@page.post('/update-order-status')
def update_order_stats() :

    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return jsonify({"message": "Tu dois être connecté pour accéder à cette fonctionnalité."}), 401

    data = request.json
    order_id = data['order_id']
    status = data["status"]
    order = db.session.scalar(db.select(Order).where(Order.id == order_id))
    status = db.session.scalar(db.select(OrderStatus).where(OrderStatus.state == status))

    if order is None:
        return jsonify({"message": "Aucune commande n'existe avec cet ID."}), 400
    if status is None:
        return jsonify({"message": "Le status entré est invalide."}), 400

    try:
        order.status = status
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "Le statut de la commande a bien été changé.", "status": status.state}), 200

@page.post('/update-tag-color')
def update_tag_color():

    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return jsonify({"message": "Tu dois être connecté pour accéder à cette fonctionnalité."}), 401
    
    data = request.json
    tag_id = data["tag_id"]
    color = data["color"].lower()
    tag = db.session.scalar(db.select(Tag).where(Tag.id == tag_id))

    if tag is None:
        return jsonify({"message": "Aucun tag n'existe avec cet ID."}), 400
    if re.match(r'^[0-9a-fA-F]{6}$', color) is None:
        return jsonify({"message": "Le format de la couleur est invalide."}), 400

    try:
        tag.color = color
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La couleur du tag a bien été changée.", "color": color}), 200

@page.post('/update-ingredient-color')
def update_ingredient_color():

    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return jsonify({"message": "Tu dois être connecté pour accéder à cette fonctionnalité."}), 401
    
    data = request.json
    ingredient_id = data["ingredient_id"]
    color = data["color"].lower()
    ingredient = db.session.scalar(db.select(Ingredient).where(Ingredient.id == ingredient_id))

    if ingredient is None:
        return jsonify({"message": "Aucun ingrédient n'existe avec cet ID."}), 400
    if re.match(r'^[0-9a-fA-F]{6}$', color) is None:
        return jsonify({"message": "Le format de la couleur est invalide."}), 400

    try:
        ingredient.color = color
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La couleur de l'ingrédient a bien été changée.", "color": color}), 200

@page.post('/update-ingredient-category')
def update_ingredient_category():

    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return jsonify({"message": "Tu dois être connecté pour accéder à cette fonctionnalité."}), 401
    
    data = request.json
    ingredient_id = data["ingredient_id"]
    category = data["category"].lower()
    ingredient = db.session.scalar(db.select(Ingredient).where(Ingredient.id == ingredient_id))
    category = db.session.scalar(db.select(IngredientCategory).where(IngredientCategory.name == category))

    if ingredient is None:
        return jsonify({"message": "Aucun ingrédient n'existe avec cet ID."}), 400
    if category is None:
        return jsonify({"message": "La catégorie indiquée est invalide."}), 400

    try:
        ingredient.category = category
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La catégorie de l'ingrédient a bien été changée.", "category": category.name}), 200
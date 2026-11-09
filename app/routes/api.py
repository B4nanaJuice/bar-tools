from flask import Blueprint, request, jsonify, session, send_file
from flask_limiter.errors import RateLimitExceeded
import os 
import re
import json
from functools import wraps

from app.database import db
from app.models import Cocktail, Tag, Ingredient, Order, OrderItem, OrderStatus, IngredientCategory

page = Blueprint("api", __name__, url_prefix = '/api')

@page.errorhandler(429)
def too_many_requests(e: RateLimitExceeded):
    return jsonify({"message": "Too many requests"}), 429

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
            return jsonify({"message": "Tu n'as pas la permission d'entrer ici, es-tu sûr(e) que tu ne t'es pas perdu(e) ?"}), 401
        return func(*args, **kwargs)
    return decorated_function

def check_format(value, expected_type) -> bool:

    if expected_type in [int, float, str]:
        return isinstance(value, expected_type)

    elif isinstance(expected_type, dict):
        if not isinstance(value, dict):
            return False
        
        if set(value.keys()) != set(expected_type.keys()):
            return False
        
        return all([check_format(value.get(k), expected_type.get(k)) for k in expected_type.keys()])

    elif isinstance(expected_type, list):
        if not isinstance(value, list):
            return False
        
        return all([check_format(_, expected_type[0]) for _ in value])

def body_format_required(struct):
    # Exemples :
    # Simple values :      {"key1": int}, {"key1": str}
    # Sub-dicts :          {"key1": {"key11": int}}
    # Simple lists :       {"key1": [int]}, {"key1": [str]}
    # Lists of sub-dicts : {"key1": [{"key11": str, "key12": int}]}
    def body_format_required(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            data = request.json # Get the body
            if not check_format(data, struct):
                return jsonify({"message": "Les données envoyées au serveur ne correspondent pas à la structure attendue."}), 400
            return func(*args, **kwargs)
        return decorated_function
    return body_format_required

@page.post("/send-order")
@body_format_required({"name": str, "content": [{"cocktail_id": int, "quantity": int}]})
def send_order():

    data = request.json
    customer_name: str = data.get("name")

    order = Order(customer_name = customer_name)
    db.session.add(order)
    db.session.flush()

    order_content = data.get("content")
    for order_item in order_content:

        try:
            cocktail_id = int(order_item["cocktail_id"])
            quantity: int = int(order_item["quantity"])

            cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == cocktail_id))

            if cocktail is None:
                return jsonify({"message": "Le cocktail demandé est invalide. Vérifie ton panier avant de recommencer."}), 404

            assert quantity > 0, "Quantité invalide. Vérifie ton panier avant de recommencer."

            db.session.add(
                OrderItem(
                    order = order,
                    cocktail = cocktail,
                    quantity = quantity
                )
            )

        except Exception as e:
            return jsonify({"message": e}), 400

    db.session.commit()

    return jsonify({"message": "Ta commande a bien été passée ! Tu recevras bientôt ce que tu as demandé.", "orderId": order.id}), 200

@page.post('/update-order-status')
@body_format_required({"order_id": int, "status": str})
@admin_required
def update_order_status() :

    data = request.json
    order_id = data.get("order_id")
    status = data.get("status")

    order = db.session.scalar(db.select(Order).where(Order.id == order_id))
    status = db.session.scalar(db.select(OrderStatus).where(OrderStatus.state == status))

    if order is None:
        return jsonify({"message": "Aucune commande n'existe avec cet ID."}), 404
    if status is None:
        return jsonify({"message": "Le status entré est invalide."}), 404

    try:
        order.status = status
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "Le statut de la commande a bien été changé.", "state": status.state}), 200

@page.post('/update-tag-color')
@body_format_required({"tag_id": int, "color": str})
@admin_required
def update_tag_color():
    
    data = request.json
    tag_id = data.get("tag_id")
    color = (data.get("color") or "ffffff").lower()
    tag = db.session.scalar(db.select(Tag).where(Tag.id == tag_id))

    if tag is None:
        return jsonify({"message": "Aucun tag n'existe avec cet ID."}), 404
    if re.match(r'^[0-9a-fA-F]{6}$', color) is None:
        return jsonify({"message": "Le format de la couleur est invalide."}), 400

    try:
        tag.color = color
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La couleur du tag a bien été changée.", "color": color}), 200

@page.post('/update-ingredient-color')
@body_format_required({"ingredient_id": int, "color": str})
@admin_required
def update_ingredient_color():
    
    data = request.json
    ingredient_id = data.get("ingredient_id")
    color = (data.get("color") or "ffffff").lower()
    ingredient = db.session.scalar(db.select(Ingredient).where(Ingredient.id == ingredient_id))

    if ingredient is None:
        return jsonify({"message": "Aucun ingrédient n'existe avec cet ID."}), 404
    if re.match(r'^[0-9a-fA-F]{6}$', color) is None:
        return jsonify({"message": "Le format de la couleur est invalide."}), 400

    try:
        ingredient.color = color
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La couleur de l'ingrédient a bien été changée.", "color": color}), 200

@page.post('/update-ingredient-category')
@body_format_required({"ingredient_id": int, "category": str})
@admin_required
def update_ingredient_category():
    
    data = request.json
    ingredient_id = data.get("ingredient_id")
    category = (data.get("category") or "other").lower()
    ingredient = db.session.scalar(db.select(Ingredient).where(Ingredient.id == ingredient_id))
    category = db.session.scalar(db.select(IngredientCategory).where(IngredientCategory.name == category))

    if ingredient is None:
        return jsonify({"message": "Aucun ingrédient n'existe avec cet ID."}), 404
    if category is None:
        return jsonify({"message": "La catégorie indiquée est invalide."}), 404

    try:
        ingredient.category = category
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "La catégorie de l'ingrédient a bien été changée.", "category": category.name}), 200

@page.post('/update-cocktail-image')
@body_format_required({"cocktail_id": int, "image": str})
@admin_required
def update_cocktail_image():

    data = request.json
    cocktail_id = data.get("cocktail_id")
    image = data.get("image")
    cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == cocktail_id))

    if cocktail is None:
        return jsonify({"message": "Aucun cocktail n'existe avec cet ID."}), 404

    try:
        cocktail.image = image
        db.session.commit()
    except:
        return jsonify({"message": "Quelque chose s'est mal passé..."}), 400

    return jsonify({"message": "L'image du cocktail a bien été changée !", "image": image}), 200
    

@page.get('/get-order-status')
def get_order_status():

    try:
        order_id = request.args.get("order-id")
        order_id = int(order_id)

        order = db.session.scalar(db.select(Order).where(Order.id == order_id))

        if order is None:
            return jsonify({"state": None}), 404

        return jsonify({"state": order.status.to_dict()}), 200
    except:
        return jsonify({"state": None}), 400

@page.get('/get-cocktail')
def get_cocktail():

    try:
        cocktail_id = request.args.get("cocktail-id")
        cocktail_id = int(cocktail_id)

        cocktail = db.session.scalar(db.select(Cocktail).where(Cocktail.id == cocktail_id))

        if cocktail is None:
            return jsonify({"cocktail": None}), 404

        return jsonify({"cocktail": cocktail.to_dict()}), 200
    except:
        return jsonify({"cocktail": None}), 400

@page.get('/get-ingredients')
def get_ingredients():
    ingredients = Ingredient.query.where(Ingredient.is_available).order_by(Ingredient.name).all()
    return jsonify({"ingredients": [_.to_dict() for _ in ingredients]}), 200

@page.get('/get-ingredient-categories')
def get_ingredient_categories():
    categories = IngredientCategory.query.all()
    return jsonify({"categories": [_.to_dict() for _ in categories]}), 200

@page.get('/get-tags')
def get_tags():
    tags = Tag.query.order_by(Tag.name).all()
    return jsonify({"tags": [_.to_dict() for _ in tags]}), 200

@page.get('/export-config')
@admin_required
def export_config():

    # Get data
    ingredients: list[Ingredient] = Ingredient.query.all()
    tags: list[Tag] = Tag.query.all()

    # Create file
    from datetime import datetime
    filename: str = f"app/exports/config_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.json"
    with open(filename, mode = "w", encoding = "utf-8") as fp:
        fp.write(
            json.dumps(
                obj = {
                    "ingredients": {ingredient.name: {"color": ingredient.color, "category": ingredient.category.name} for ingredient in ingredients},
                    "tags": {tag.name: {"color": tag.color} for tag in tags}
                }
            )
        )
    fp = open(filename, mode = "r+b")
    return send_file(fp, "application/json", as_attachment = True, download_name = "config.json")
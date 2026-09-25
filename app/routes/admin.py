from flask import Blueprint, render_template, url_for, request, jsonify, session, redirect
import os

from app.database import db
from app.models import Order, Ingredient

page = Blueprint("admin", __name__, url_prefix = '/admin')

@page.before_request
def check_user_login():
    if "id" not in session or session["id"] != os.environ["ADMIN_ID"]:
        return redirect(url_for("auth.login"))

@page.get("/orders")
def get_orders():

    orders = Order.query.all()

    return jsonify([f"{_}" for _ in orders])

@page.route("/stocks", methods = ["GET", "POST"])
def manage_stocks():

    ingredients: list[Ingredient] = Ingredient.query.order_by(Ingredient.name).all()

    if request.method == "POST":
        for ingredient in ingredients:
            ingredient.is_available = f"{ingredient.id}" in request.form
        db.session.commit()
        return redirect(url_for("admin.manage_stocks"))

    return render_template("stocks.html.jinja", ingredients = ingredients)
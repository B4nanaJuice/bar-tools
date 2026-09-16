from flask import Blueprint, render_template, url_for, request, jsonify

from app.database import db
from app.models import Order

page = Blueprint("admin", __name__, url_prefix = '/admin')

@page.get("/orders")
def send_order():

    orders = Order.query.all()

    return jsonify([f"{_}" for _ in orders])
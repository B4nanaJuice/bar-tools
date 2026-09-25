from flask import Blueprint, render_template, url_for, request, jsonify, session, redirect
import os

page = Blueprint("auth", __name__, url_prefix = '/auth')

@page.route("/login", methods = ["GET", "POST"])
def login():

    if "id" in session and session["id"] == os.environ["ADMIN_ID"]:
        return redirect(url_for("admin.get_orders"))

    if request.method == "POST":
        user_login = request.form.get("id")
        user_password = request.form.get("password")

        if user_login != os.environ["ADMIN_ID"] or user_password != os.environ["ADMIN_PASSWORD"]:
            return "Invalid credentials"

        session["id"] = user_login
        return redirect(url_for("admin.get_orders"))
    
    return "<form method=\"post\"><input name=\"id\" id=\"id\"><input name=\"password\" id=\"password\"><input type=\"submit\"></form>"
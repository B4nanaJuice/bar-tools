from flask import Blueprint, url_for, request, session, redirect, render_template
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

    return render_template("login.html.jinja", page_type = "other")

@page.get("/logout")
def logout():
    if "id" in session:
        del session["id"]
    return redirect(url_for("home.index"))
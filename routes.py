# routes.py - Flask-Routen
from flask import render_template, session, request, redirect
from auth import login, callback, logout
from database import get_user, save_user
from decrypt_enc_PIN import encrypt_pin
def configure_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")
    @app.route("/login")
    def login_route():
        return login()
    @app.route("/login/callback")
    def callback_route():
        return callback()
    @app.route("/logout")
    def logout_route():
        return logout()
    @app.route("/dashboard")
    def dashboard():
        email = session.get("email")
        if not email:
            return redirect("/")
        user_doc = get_user(email)
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return render_template("dashboard.html", konto=user_data.get("bank_identifier"), saldo="Unbekannt")
        return redirect("/fints_login")
    @app.route("/fints_login", methods=["GET", "POST"])
    def fints_login():
        if request.method == "POST":
            bank_identifier = request.form["bank_identifier"]
            user_id = request.form["user_id"]
            pin = request.form["pin"]
            server = request.form["server"]
            save_user(session["email"], {"bank_identifier": bank_identifier, "user_id": user_id, "pin": encrypt_pin(pin), "server": server})
            return redirect("/dashboard")
        return render_template("fints_login.html")
# app.py - Hauptanwendung
import os
from flask import Flask
from routes import configure_routes

app = Flask(__name__)
app.secret_key = os.urandom(24)

configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
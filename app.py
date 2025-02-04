from flask import Flask, render_template, request
import logging
from fints.client import FinTS3PinTanClient, NeedTANResponse

app = Flask(__name__)

# Produkt-ID fest im Code hinterlegt
PRODUCT_ID = "36792786FA12F235F04647689"

# Logging deaktivieren
logging.basicConfig(level=logging.ERROR)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Formulardaten auslesen
        server = request.form["server"]
        bank_identifier = request.form["bank_identifier"]
        user_id = request.form["user_id"]
        pin = request.form["pin"]

        # FinTS-Client erstellen
        f = FinTS3PinTanClient(
            bank_identifier=bank_identifier,
            user_id=user_id,
            pin=pin,
            server=server,
            product_id=PRODUCT_ID
        )

        with f:
            # Falls eine TAN nötig ist
            if f.init_tan_response:
                return render_template("tan.html", challenge=f.init_tan_response.challenge)

            # Konten abrufen
            accounts = f.get_sepa_accounts()
            if not accounts:
                return "Keine Konten gefunden.", 400
            
            # Ersten Kontosaldo abrufen
            saldo = f.get_balance(accounts[0])

        return render_template("konto.html", konto=accounts[0].iban, saldo=saldo.amount)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
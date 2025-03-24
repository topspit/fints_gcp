import os
import pathlib
import requests
from flask import Flask, session, redirect, request, render_template, abort, jsonify
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from functools import wraps
from fints.client import FinTS3PinTanClient, NeedTANResponse
import firebase_admin
from firebase_admin import credentials, firestore
from decrypt_enc_PIN import decrypt_pin, encrypt_pin
from google.oauth2 import service_account
from datetime import datetime, timedelta
import uuid



app = Flask(__name__)
app.secret_key = os.urandom(24)  # Geheime Session-Key

# Dictionary zur Speicherung aktiver TAN-Sessions
tan_sessions = {}

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Lokale HTTP-Entwicklung erlauben



client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "/secrets/OAUTH_CLIENT_SECRET/SECRET")


file_firestone_secret_manager = "/secrets/SERVICE_ACCOUNT_KEY/KEY"

cred = credentials.Certificate(file_firestone_secret_manager)

# Firebase-App initialisieren
firebase_admin.initialize_app(cred)

# Firestore-Client erstellen
db = firestore.client()

#FINTSClient-Product-ID
product_id = "36792786FA12F235F04647689"


# OAuth 2.0 Flow einrichten
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://fints-dev-2758660863.europe-west3.run.app/login/callback"
)



# Login-Required Decorator
def login_required(f):
    @wraps(f)  # Bewahrt den Namen und die Metadaten der Originalfunktion
    def decorated_function(*args, **kwargs):
        if "google_id" not in session:
            return redirect("/")  # Falls nicht eingeloggt, zurück zur Startseite
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/login/callback")
def callback():
    state_from_session = session.get("state")  # Sicher abrufen, ohne KeyError
    state_from_request = request.args.get("state")

    # Überprüfen, ob "state" fehlt
    if not state_from_session or state_from_session != state_from_request:
        return redirect("/logout")  # Oder eine Fehlermeldung anzeigen

    # Wenn der State stimmt, OAuth-Flow fortsetzen...
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=flow.client_config["client_id"]
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email") # speicherung eMail
    print(session["email"])
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@app.route("/dashboard")
@login_required
def dashboard():
    session["FINTS_client"] = {}
    email = session.get("email")
    if not email:
        return redirect("/")
    user_ref = db.collection("known_users").document(email)
    user_doc = user_ref.get()

    
    if user_doc.exists:
        # Falls der Nutzer existiert, die gespeicherten Daten abrufen
        user_data = user_doc.to_dict()
        bank_identifier = user_data["bank_identifier"]
        user_id = user_data["user_id"]
        pin = decrypt_pin(user_data["pin"])
        server = user_data["server"]

        # Falls eine laufende TAN-Session existiert, nutze den gespeicherten Client
        fints_client = session.get("FINTS_client")
        if fints_client is not None:
            f = session["FINTS_client"]
            
        else:
            # Objekt existiert nicht
            f = FinTS3PinTanClient(
                bank_identifier=bank_identifier,
                user_id=user_id,
                pin=pin,
                server=server,
                product_id=product_id
            )
            session["FINTS_client"] = f

        
        with f:
            # Falls eine TAN nötig ist für den Log-In
            if f.init_tan_response:
                return render_template("tan.html", challenge=f.init_tan_response.challenge)

            # Konten abrufen
            accounts = f.get_sepa_accounts()
            if not accounts:
                return "Keine Konten gefunden.", 400
            
            # Ersten Kontosaldo abrufen
            saldo = f.get_balance(accounts[0])
            

        return render_template("dashboard.html", konto=accounts[0].iban, saldo=saldo.amount)

    else:
        print(f"email ist NICHT in mock?")
        return redirect("/fints_login")

@app.route("/fints_login", methods=["GET", "POST"])
@login_required
def fints_login():
    if request.method == "POST":
        #print(f"sind wohl im fint_login_post")
        bank_identifier = request.form["bank_identifier"]
        user_id = request.form["user_id"]
        pin = request.form["pin"]
        server = request.form["server"]

        # FINTS Login durchführen
        f = FinTS3PinTanClient(
            bank_identifier=bank_identifier,
            user_id=user_id,
            pin=pin,
            server=server,
            product_id=product_id
        )
        session["fints_client"] = f
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
            # Daten in Firestore speichern
            user_data = {
            "bank_identifier": bank_identifier,
            "user_id": user_id,
            "pin": encrypt_pin(pin),  # Achtung: Unsicher, besser verschlüsseln!
            "server": server
            }
            email = session["email"]
            db.collection("known_users").document(email).set(user_data)
            #print("Datenbankschreiben scheint geklappt zu haben")
        return render_template("dashboard.html", konto=accounts[0].iban, saldo=saldo.amount)

        

    return render_template("fints_login.html")

@app.route("/transactions", methods=["POST"])
@login_required
def get_transactions():
    email = session.get("email")
    if not email:
        return redirect("/")
    selected_days = int(request.form["days"])
    start_date = datetime.today() - timedelta(days=selected_days)

    
    user_ref = db.collection("known_users").document(email)
    user_doc = user_ref.get()
    tan_session_id = request.form["tan_session_id"]
    tan_data = tan_sessions.pop(tan_session_id)
    
    
    f = tan_data["client"]  # FinTS3PinTanClient

    with f:
        # Falls eine TAN nötig ist
        if f.init_tan_response:
            return render_template("tan.html", challenge=f.init_tan_response.challenge)

        accounts = f.get_sepa_accounts()
        if not accounts:
            return "Keine Konten gefunden.", 400

        saldo = request.form["saldo"]
        transactions = f.get_transactions(accounts[0], start_date=start_date)
        
        # Falls eine TAN erforderlich ist
        if isinstance(transactions, NeedTANResponse):
            return render_template("dashboard.html", saldo=saldo, selected_days=selected_days,
                                   tan_challenge=transactions.challenge, tan_session_id=tan_session_id)

    # Transaktionsdaten für das HTML umformatieren
    transaction_list = []
    for tx in transactions:
        data = tx.data
        transaction_list.append({
            "date": data["date"],
            "applicant_name": data["applicant_name"],
            "amount": data["amount"],
            "purpose": data["purpose"]
        })

    return render_template("dashboard.html", saldo=saldo, transactions=transaction_list, selected_days=selected_days)

@app.route("/send_tan", methods=["POST"])
@login_required
def send_tan():
    if "email" not in session:
        return redirect("/")

    tan = request.form["tan"]
    tan_session_id = request.form["tan_session_id"]
    saldo = request.form["saldo"]

    # Prüfen, ob die TAN-Session existiert
    if tan_session_id not in tan_sessions:

        print(f"Session nicht wiedergefunden")
        return "Fehler: TAN-Session nicht gefunden.", 400

    #Hole den gespeicherten Client und NeedTANResponse
    tan_data = tan_sessions.pop(tan_session_id)
    f = tan_data["client"]  # FinTS3PinTanClient
    transactions = tan_data["transactions"]  # NeedTANResponse
    print(f"Typ von transactions: {type(transactions)}")

    try:
        transactions = f.send_tan(transactions, tan)
        
        
    except Exception as e:
        return f"Fehler beim Senden der TAN: {str(e)}", 500  

    return show_transactions(transactions, request.form["days"], saldo)


def show_transactions(transactions, selected_days, saldo):
    """Hilfsfunktion zur Darstellung der Transaktionsliste"""
    transaction_list = []
    for tx in transactions:
        data = tx.data
        transaction_list.append({
            "date": data["date"],
            "applicant_name": data["applicant_name"],
            "amount": data["amount"],
            "purpose": data["purpose"]
        })

    return render_template("dashboard.html", saldo=saldo, transactions=transaction_list, selected_days=selected_days)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
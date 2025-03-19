# database.py - Firestore-Datenbank
import firebase_admin
from firebase_admin import credentials, firestore

file_firestone_secret_manager = "secrets/SERVICE_ACCOUNT_KEY/KEY"
cred = credentials.Certificate(file_firestone_secret_manager)
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_user(email):
    return db.collection("known_users").document(email).get()

def save_user(email, data):
    db.collection("known_users").document(email).set(data)
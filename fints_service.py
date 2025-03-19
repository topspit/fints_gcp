# fints_service.py - FINTS-Funktionen
from fints.client import FinTS3PinTanClient
from decrypt_enc_PIN import decrypt_pin, encrypt_pin

product_id = "36792786FA12F235F04647689"

def login_fints(bank_identifier, user_id, pin, server):
    f = FinTS3PinTanClient(
        bank_identifier=bank_identifier,
        user_id=user_id,
        pin=pin,
        server=server,
        product_id=product_id
    )
    with f:
        if f.init_tan_response:
            return {"tan_required": True, "challenge": f.init_tan_response.challenge}
        accounts = f.get_sepa_accounts()
        if not accounts:
            return {"error": "Keine Konten gefunden."}
        saldo = f.get_balance(accounts[0])
        return {"konto": accounts[0].iban, "saldo": saldo.amount}
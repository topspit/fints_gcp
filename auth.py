# auth.py - OAuth-Authentifizierung
import os
import pathlib
import requests
from flask import session, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

oauth_secrets_file = os.path.join(pathlib.Path(__file__).parent, "secrets/OAUTH_CLIENT_SECRET/SECRET")
flow = Flow.from_client_secrets_file(
    client_secrets_file=oauth_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://fints-dev-2758660863.europe-west3.run.app/login/callback"
)

def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

def callback():
    state_from_session = session.get("state")
    state_from_request = request.args.get("state")
    if not state_from_session or state_from_session != state_from_request:
        return redirect("/logout")
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
    session["email"] = id_info.get("email")
    return redirect("/dashboard")

def logout():
    session.clear()
    return redirect("/")
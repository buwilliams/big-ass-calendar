from flask import Blueprint, redirect, url_for, session, current_app, request, jsonify
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os
import copy

auth_bp = Blueprint("auth", __name__)

# Google OAuth scopes needed for calendar access
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

@auth_bp.route("/login")
def login():
    # Get a copy of the client config and add dynamic redirect URI
    client_config = copy.deepcopy(current_app.config["GOOGLE_CLIENT_CONFIG"])
    
    # Ensure the redirect URI is set correctly (dynamically based on current request)
    if "web" in client_config:
        client_config["web"]["redirect_uris"] = [url_for("auth.oauth2callback", _external=True)]
    
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        SCOPES
    )
    
    authorization_url, state = flow.authorization_url(
        access_type="offline", 
        include_granted_scopes="true"
    )
    
    session["state"] = state
    
    return redirect(authorization_url)

@auth_bp.route("/oauth2callback")
def oauth2callback():
    state = session.get("state")
    
    if not state or state != request.args.get("state"):
        return jsonify({"error": "State mismatch"}), 400
    
    # Get a copy of the client config and add dynamic redirect URI
    client_config = copy.deepcopy(current_app.config["GOOGLE_CLIENT_CONFIG"])
    
    # Ensure the redirect URI is set correctly (dynamically based on current request)
    if "web" in client_config:
        client_config["web"]["redirect_uris"] = [url_for("auth.oauth2callback", _external=True)]
    
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        SCOPES,
        state=state
    )
    
    flow.redirect_uri = url_for("auth.oauth2callback", _external=True)
    
    # Get authorization code from request
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    # Store credentials in session
    credentials = flow.credentials
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
    
    return redirect(url_for("calendar.index"))

@auth_bp.route("/logout")
def logout():
    if "credentials" in session:
        del session["credentials"]
    
    return redirect(url_for("calendar.index"))

@auth_bp.route("/check-auth")
def check_auth():
    if "credentials" in session:
        return jsonify({"authenticated": True})
    return jsonify({"authenticated": False})
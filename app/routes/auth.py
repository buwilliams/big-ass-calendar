from flask import Blueprint, redirect, url_for, session, current_app, request, jsonify
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import os

auth_bp = Blueprint("auth", __name__)

# Google OAuth scopes needed for calendar access
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events"
]

@auth_bp.route("/login")
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": current_app.config["GOOGLE_CLIENT_ID"],
                "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
                "redirect_uris": [url_for("auth.oauth2callback", _external=True)],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
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
    
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
            "web": {
                "client_id": current_app.config["GOOGLE_CLIENT_ID"],
                "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
                "redirect_uris": [url_for("auth.oauth2callback", _external=True)],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
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
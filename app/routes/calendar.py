from flask import Blueprint, render_template, session, jsonify, request, current_app
import google.oauth2.credentials
from googleapiclient.discovery import build
from app.services.calendar_service import get_events_for_year, update_event_note
from datetime import datetime

calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/")
def index():
    """Render the main application page"""
    # Pass app title from config to the template
    return render_template(
        "index.html", 
        app_title=current_app.config.get("APP_TITLE", "The Big A$$ Calendar"),
        default_year=current_app.config.get("DEFAULT_YEAR", datetime.now().year)
    )
    
@calendar_bp.route('/favicon.ico')
def favicon():
    """Serve the favicon from the root path"""
    return current_app.send_static_file('img/favicon.ico')

@calendar_bp.route("/api/config")
def get_app_config():
    """Return client-side configuration"""
    return jsonify({
        "title": current_app.config.get("APP_TITLE", "The Big A$$ Calendar"),
        "defaultYear": current_app.config.get("DEFAULT_YEAR", datetime.now().year)
    })

@calendar_bp.route("/api/calendars")
def get_calendars():
    """Get user's calendar list from Google Calendar API"""
    if "credentials" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    service = build("calendar", "v3", credentials=credentials)
    
    calendar_list = service.calendarList().list().execute()
    
    calendars = []
    for calendar in calendar_list.get("items", []):
        calendars.append({
            "id": calendar["id"],
            "summary": calendar["summary"],
            "backgroundColor": calendar.get("backgroundColor", "#4285F4"),
            "foregroundColor": calendar.get("foregroundColor", "#FFFFFF"),
            "selected": calendar.get("selected", True)
        })
    
    # Update session credentials (they might have been refreshed)
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
    
    return jsonify(calendars)

@calendar_bp.route("/api/events")
def get_events():
    """Get events for a specific year from Google Calendar API"""
    if "credentials" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Get year from query params or use default from config
    default_year = current_app.config.get("DEFAULT_YEAR", datetime.now().year)
    year = request.args.get("year", default_year)
    try:
        year = int(year)
    except ValueError:
        return jsonify({"error": "Invalid year parameter"}), 400
    
    calendar_ids = request.args.getlist("calendar_id")
    if not calendar_ids:
        return jsonify({"error": "No calendar IDs provided"}), 400
    
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    
    events = get_events_for_year(credentials, year, calendar_ids)
    
    # Update session credentials (they might have been refreshed)
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
    
    return jsonify(events)

@calendar_bp.route("/api/events/<event_id>/note", methods=["PUT"])
def update_note(event_id):
    """Update a note for a specific event"""
    if "credentials" not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    if not data or "note" not in data:
        return jsonify({"error": "Note data is required"}), 400
    
    calendar_id = request.args.get("calendar_id")
    if not calendar_id:
        return jsonify({"error": "Calendar ID is required"}), 400
    
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])
    
    success = update_event_note(credentials, calendar_id, event_id, data["note"])
    
    # Update session credentials (they might have been refreshed)
    session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes
    }
    
    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Failed to update event note"}), 500
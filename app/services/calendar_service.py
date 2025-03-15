from googleapiclient.discovery import build
from datetime import datetime, timedelta
import re

def get_events_for_year(credentials, year, calendar_ids):
    """
    Fetch all events for the specified year from the given Google calendars.
    
    Args:
        credentials: Google OAuth credentials
        year: The year to fetch events for (integer)
        calendar_ids: List of calendar IDs to fetch events from
        
    Returns:
        Dictionary of events organized by date
    """
    service = build("calendar", "v3", credentials=credentials)
    
    # Set time boundaries for the year
    start_date = datetime(year, 1, 1, 0, 0, 0).isoformat() + "Z"
    end_date = datetime(year, 12, 31, 23, 59, 59).isoformat() + "Z"
    
    all_events = []
    
    for calendar_id in calendar_ids:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        
        for event in events:
            # Add calendar ID to each event for reference
            event["calendarId"] = calendar_id
            
            # Extract the note if it exists in the description
            note = extract_note_from_description(event.get("description", ""))
            if note:
                event["note"] = note
            
            all_events.append(event)
    
    # Organize events by date for easier frontend processing
    events_by_date = {}
    
    for event in all_events:
        start = event.get("start", {})
        
        # Handle all-day events
        if "date" in start:
            event_date = start["date"]
        else:
            # Convert datetime to date string
            event_datetime = start.get("dateTime", "")
            if event_datetime:
                dt = datetime.fromisoformat(event_datetime.replace("Z", "+00:00"))
                event_date = dt.strftime("%Y-%m-%d")
            else:
                continue  # Skip events with no date
        
        # Add event to the appropriate date
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        
        events_by_date[event_date].append(event)
    
    return events_by_date

def update_event_note(credentials, calendar_id, event_id, note):
    """
    Update the note section of an event's description.
    
    Args:
        credentials: Google OAuth credentials
        calendar_id: ID of the calendar containing the event
        event_id: ID of the event to update
        note: New note content
        
    Returns:
        Boolean indicating success
    """
    service = build("calendar", "v3", credentials=credentials)
    
    try:
        # Get the current event
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        # Update the description with the new note
        description = event.get("description", "")
        
        # Check if there's already a note section
        note_pattern = r"(<!-- BIGASSCALENDAR_NOTE_START -->.*<!-- BIGASSCALENDAR_NOTE_END -->)"
        note_section = f"<!-- BIGASSCALENDAR_NOTE_START -->{note}<!-- BIGASSCALENDAR_NOTE_END -->"
        
        if re.search(note_pattern, description, re.DOTALL):
            # Replace existing note
            updated_description = re.sub(note_pattern, note_section, description, flags=re.DOTALL)
        else:
            # Add new note at the end
            if description:
                updated_description = description + "\n\n" + note_section
            else:
                updated_description = note_section
        
        # Update the event
        event["description"] = updated_description
        
        service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event
        ).execute()
        
        return True
        
    except Exception as e:
        print(f"Error updating event note: {e}")
        return False

def extract_note_from_description(description):
    """
    Extract the note section from an event description.
    
    Args:
        description: Event description text
        
    Returns:
        Note text if found, otherwise None
    """
    if not description:
        return None
    
    note_pattern = r"<!-- BIGASSCALENDAR_NOTE_START -->(.*?)<!-- BIGASSCALENDAR_NOTE_END -->"
    match = re.search(note_pattern, description, re.DOTALL)
    
    if match:
        return match.group(1)
    
    return None
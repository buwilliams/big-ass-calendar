# Big Ass Calendar

A web application that displays an entire year's schedule in a single view. The application provides an intuitive, elegant interface allowing users to see their entire year at a glance while maintaining the ability to zoom in on specific dates and view detailed event information.

## Features

- Year-at-a-glance grid layout (months as rows, days as columns)
- Google Calendar integration
- Intuitive zoom and pan navigation
- Mobile support with touch gestures (pinch-to-zoom, drag)
- View and add notes to events
- Toggle different calendars on/off

## Technology Stack

- **Backend**: Python with Flask
- **Frontend**: Alpine.js for UI logic, HTML5 Canvas for calendar rendering
- **APIs**: Google Calendar API for fetching and updating events

## Setup and Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `config.yaml` file based on `config_sample.yaml` and add your Google API credentials:
   ```
   cp config_sample.yaml config.yaml
   # Edit config.yaml with your settings
   ```
5. Run the application:
   ```
   python run.py
   ```

You can also specify a custom config file location:
```
python run.py --config=/path/to/custom/config.yaml
```

## Google API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Web application type)
5. Add authorized redirect URIs:
   - `http://localhost:5000/oauth2callback` (for development)
   - Your production callback URL when deployed
6. Download the client credentials JSON file by clicking the "Download JSON" button
7. Save the file as `google_client.json` in the project root directory

Alternatively, you can add the credentials to your `config.yaml` file:

```yaml
google:
  client_id: "your-client-id-here"
  client_secret: "your-client-secret-here"
```

The application will prefer the `google_client.json` file if it exists.

## Usage

1. Open the application in your browser
2. Click "Sign in with Google" to authenticate
3. Choose which calendars to display using the Calendars button
4. Navigate through years using the arrows
5. Zoom in/out using:
   - Desktop: mouse wheel or trackpad gestures
   - Mobile: pinch gestures
6. Pan around the calendar using:
   - Desktop: click and drag
   - Mobile: touch and drag
7. Click on a date to view detailed events
8. Add notes to events in the side panel

## Development

- Format code: `black .`
- Run linting: `flake8`
- Type checking: `mypy .`
- Run tests: `pytest`

## License

MIT
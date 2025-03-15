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

### Local Development

This project includes a simplified version of Alpine.js for local development. For production use, download the complete library:

```bash
# From the project root
curl -o app/static/js/vendor/alpine.min.js https://unpkg.com/alpinejs@3.13.3/dist/cdn.min.js
```

The application is configured to use the local file and fall back to the CDN if necessary.

## Setup and Installation

### Quick Start (Linux/Mac)

Use the included shell script to automatically set up and run the application:

```bash
# Make the script executable (first time only)
chmod +x run.sh

# Run the application
./run.sh
```

The script will:
1. Create a virtual environment if it doesn't exist
2. Install all dependencies
3. Create config files from samples if they don't exist
4. Run the application with the correct parameters

### Manual Setup

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
4. Create a `config.yaml` file based on `config_sample.yaml`:
   ```
   cp config_sample.yaml config.yaml
   # Edit config.yaml with your settings
   ```
5. Create a `google_client.json` file based on the sample or download it from Google Cloud Console:
   ```
   cp google_client_sample.json google_client.json
   # Edit google_client.json with your credentials
   ```
6. Run the application:
   ```
   python run.py
   ```

### Advanced Usage

You can specify custom file locations:
```
python run.py --config=/path/to/custom/config.yaml --google-client=/path/to/credentials.json
```

For more information about available options:
```
python run.py --info
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
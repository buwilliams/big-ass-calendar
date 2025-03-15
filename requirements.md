# Project Brief: Big Ass Calendar

## Overview
Create a web application that displays an entire year's schedule in a single view. The application should provide an intuitive, elegant interface allowing users to see their entire year at a glance while maintaining the ability to zoom in on specific dates and view detailed event information.

## Core Concept
The "Big Ass Calendar" is designed around a year-at-a-glance grid layout where:
- Columns represent the days of the month (1-31)
- Rows represent months (January-December)
- Each cell contains events for that specific day

## Business Requirements

### Primary View
1. Create a grid layout where:
   - Horizontal axis shows days of the month (1-31)
   - Vertical axis shows months (January-December)
   - Each cell displays events for that specific day

2. Implement intuitive navigation:
   - Mobile: Support pinch-to-zoom in/out and drag gestures
   - Desktop: Support mouse wheel zoom in/out and click-and-drag panning
   - Ensure smooth, responsive interactions

3. Google Calendar integration:
   - Implement Google Sign-in functionality
   - Fetch and display the user's Google Calendar events
   - Allow users to toggle different calendars on/off
   - Support adding notes to events that sync back to Google Calendar

4. UI Elements:
   - Year selector with prev/next buttons to navigate between years
   - Calendar title showing "The Big A$$ Calendar" and current year
   - Dropdown or sidebar showing available Google Calendars with toggle switches
   - Logout button
   - Day selection to view detailed events
   - Panel/modal for displaying and editing event details

5. Interface Design:
   - Clean, minimalist aesthetic with focus on readability
   - Implement gestalt principles for intuitive visual grouping
   - Use appropriate color coding for different calendars/event types
   - Ensure adequate spacing and visual hierarchy

### Detailed Interactions
1. When a user clicks/taps on a day cell:
   - Open a side panel or modal showing all events for that day
   - Display event details including title, time, description, and location
   - Allow adding/editing notes for specific events

2. For calendar list:
   - Show all available Google Calendars with color indicators
   - Implement toggle switches to show/hide specific calendars
   - Changes should update the view immediately

3. For year navigation:
   - Provide clear buttons to move forward/backward through years
   - Ensure the transition is smooth and maintains the user's current zoom level

## Technical Requirements

### Backend
- Use Python with Flask framework
- Implement Google Calendar API integration
- Create necessary endpoints for:
  - Authentication and authorization
  - Fetching calendar data
  - Updating event notes
  - Managing user preferences

### Frontend
- Use Alpine.js for the main application logic and DOM manipulation
- Implement the calendar grid using HTML5 Canvas
- Core technical components:
  1. Canvas-based grid rendering system for the calendar view
  2. Zoom and pan functionality using canvas transformations
  3. Alpine.js for UI controls, modals, and non-canvas elements
  4. API integration with backend services

### Implementation Notes
- The canvas should handle drawing the grid, events, and handling zoom/pan gestures
- Alpine.js should manage the surrounding UI, event details panel, and user controls
- Implement appropriate data caching to improve performance
- Ensure responsive design works across different device sizes

## Sample Layout
```
|--------------------------------------------------|
| <Year> The Big A$$ Calendar                      |
|--------------------------------------------------|
| Jan | 01 | 02 | 03 | 04 | 05 | 06 | 07 | .. | 31 |
|--------------------------------------------------|
| Feb | 01 | 02 | 03 | 04 | 05 | 06 | 07 | .. | 31 |
|--------------------------------------------------|
| ... | 01 | 02 | 03 | 04 | 05 | 06 | 07 | .. | 31 |
|--------------------------------------------------|
| Dec | 01 | 02 | 03 | 04 | 05 | 06 | 07 | .. | 31 |
|--------------------------------------------------|
```

## Technical Constraints
1. Must use Python and Flask for the backend
2. Must use Alpine.js for frontend components and state management
3. Must use HTML5 Canvas for rendering the calendar grid
4. Must integrate with Google Calendar API for data
5. Must support all specified interaction methods (zoom, pan, click)

## Deliverables
1. Complete frontend and backend codebase
2. Documentation for setup and deployment
3. User guide explaining the application features
4. API documentation for the backend endpoints

As you develop this application, prioritize performance, particularly when displaying many events across the entire year, and ensure the user experience remains smooth and intuitive even on mobile devices.
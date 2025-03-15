document.addEventListener('alpine:init', () => {
    Alpine.data('calendar', (defaultYear = new Date().getFullYear()) => ({
        currentYear: defaultYear,
        isAuthenticated: false,
        calendars: [],
        selectedCalendars: [],
        events: {},
        showCalendarList: false,
        selectedDay: null,
        selectedDayEvents: [],
        appConfig: {},
        
        async init() {
            // Initialize the calendar app
            await this.fetchAppConfig();
            await this.checkAuth();
            this.setupCanvas();
            
            if (this.isAuthenticated) {
                await this.fetchCalendars();
                await this.fetchEvents();
            }
            
            // Add window resize event listener
            window.addEventListener('resize', this.debounce(() => {
                // Auto-fit when window is resized
                if (this.autoResize) {
                    this.fitCalendarToView();
                }
            }, 250));
            
            // Initialize with auto-resize enabled
            this.autoResize = true;
        },
        
        // Debounce helper function for resize events
        debounce(func, wait) {
            let timeout;
            return (...args) => {
                clearTimeout(timeout);
                timeout = setTimeout(() => func.apply(this, args), wait);
            };
        },
        
        async fetchAppConfig() {
            try {
                const response = await fetch('/api/config');
                if (response.ok) {
                    this.appConfig = await response.json();
                    document.title = this.appConfig.title;
                }
            } catch (error) {
                console.error('Error fetching app config:', error);
            }
        },
        
        async checkAuth() {
            try {
                const response = await fetch('/check-auth');
                const data = await response.json();
                this.isAuthenticated = data.authenticated;
            } catch (error) {
                console.error('Authentication check failed:', error);
                this.isAuthenticated = false;
            }
        },
        
        login() {
            window.location.href = '/login';
        },
        
        logout() {
            window.location.href = '/logout';
        },
        
        async fetchCalendars() {
            try {
                const response = await fetch('/api/calendars');
                if (!response.ok) {
                    throw new Error(`Failed to fetch calendars: ${response.statusText}`);
                }
                
                this.calendars = await response.json();
                this.selectedCalendars = this.calendars
                    .filter(cal => cal.selected)
                    .map(cal => cal.id);
                    
            } catch (error) {
                console.error('Error fetching calendars:', error);
            }
        },
        
        async fetchEvents() {
            if (this.selectedCalendars.length === 0) {
                this.events = {};
                this.drawCalendar();
                return;
            }
            
            try {
                const params = new URLSearchParams();
                params.append('year', this.currentYear);
                this.selectedCalendars.forEach(id => params.append('calendar_id', id));
                
                const response = await fetch(`/api/events?${params.toString()}`);
                if (!response.ok) {
                    throw new Error(`Failed to fetch events: ${response.statusText}`);
                }
                
                this.events = await response.json();
                this.drawCalendar();
                
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        },
        
        toggleCalendarList() {
            this.showCalendarList = !this.showCalendarList;
            if (!this.showCalendarList && this.selectedDay) {
                this.updateSelectedDayEvents();
            }
        },
        
        toggleCalendar(calendarId) {
            const index = this.selectedCalendars.indexOf(calendarId);
            if (index === -1) {
                this.selectedCalendars.push(calendarId);
            } else {
                this.selectedCalendars.splice(index, 1);
            }
            
            // Update the selected state in the calendars array
            const calendar = this.calendars.find(cal => cal.id === calendarId);
            if (calendar) {
                calendar.selected = !calendar.selected;
            }
            
            this.fetchEvents();
        },
        
        prevYear() {
            this.currentYear--;
            this.fetchEvents();
        },
        
        nextYear() {
            this.currentYear++;
            this.fetchEvents();
        },
        
        setupCanvas() {
            this.calendarCanvas = new CalendarCanvas(this.$refs.canvas);
            this.calendarCanvas.onDayClick = (day, month) => this.selectDay(day, month);
            
            // Initial draw
            this.drawCalendar();
            
            // Handle window resize
            window.addEventListener('resize', () => {
                this.calendarCanvas.resize();
                this.drawCalendar();
            });
            
            // Initial fit to view
            this.$nextTick(() => {
                this.fitCalendarToView();
            });
        },
        
        fitCalendarToView() {
            if (!this.calendarCanvas) return;
            
            // Get the container dimensions
            const container = this.$refs.canvas.parentElement;
            const containerWidth = container.clientWidth;
            const containerHeight = container.clientHeight;
            
            // Get the calendar dimensions (before any scaling or translation)
            const calendarWidth = 32 * this.calendarCanvas.columnWidth; // 31 days + 1 for month labels
            const calendarHeight = 13 * this.calendarCanvas.rowHeight; // 12 months + 1 for day labels
            
            // Calculate the scale needed to fit
            const widthScale = containerWidth / calendarWidth;
            const heightScale = containerHeight / calendarHeight;
            
            // Use the smaller scale to ensure the entire calendar fits
            let scale = Math.min(widthScale, heightScale) * 0.95; // 5% padding
            
            // Ensure scale is within reasonable bounds
            scale = Math.max(0.5, Math.min(scale, 1.5));
            
            // Reset translation and set the new scale
            this.calendarCanvas.translateX = (containerWidth - (calendarWidth * scale)) / 2;
            this.calendarCanvas.translateY = (containerHeight - (calendarHeight * scale)) / 2;
            this.calendarCanvas.scale = scale;
            
            // Redraw with new transform
            this.drawCalendar();
            
            // Provide visual feedback
            this.showResizeFeedback();
        },
        
        showResizeFeedback() {
            // Find the resize button
            const resizeBtn = document.querySelector('.highlight-btn');
            if (!resizeBtn) return;
            
            // Add a temporary class for visual feedback
            resizeBtn.classList.add('btn-flash');
            
            // Remove the class after animation completes
            setTimeout(() => {
                resizeBtn.classList.remove('btn-flash');
            }, 500);
        },
        
        drawCalendar() {
            this.calendarCanvas.drawCalendar(this.currentYear, this.events, this.calendars);
        },
        
        // Mouse and touch interactions
        startDrag(e) {
            this.calendarCanvas.startDrag(e.clientX, e.clientY);
        },
        
        drag(e) {
            this.calendarCanvas.drag(e.clientX, e.clientY);
        },
        
        endDrag() {
            this.calendarCanvas.endDrag();
        },
        
        handleZoom(e) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? -0.1 : 0.1;
            this.calendarCanvas.zoom(delta, e.clientX, e.clientY);
        },
        
        handleTouchStart(e) {
            if (e.touches.length === 1) {
                // Single touch for panning
                const touch = e.touches[0];
                this.calendarCanvas.startDrag(touch.clientX, touch.clientY);
            } else if (e.touches.length === 2) {
                // Two touches for pinch-to-zoom
                this.calendarCanvas.startPinch(e.touches);
            }
        },
        
        handleTouchMove(e) {
            e.preventDefault();
            if (e.touches.length === 1) {
                // Single touch for panning
                const touch = e.touches[0];
                this.calendarCanvas.drag(touch.clientX, touch.clientY);
            } else if (e.touches.length === 2) {
                // Two touches for pinch-to-zoom
                this.calendarCanvas.pinch(e.touches);
            }
        },
        
        handleTouchEnd() {
            this.calendarCanvas.endDrag();
            this.calendarCanvas.endPinch();
        },
        
        // Day and event handling
        selectDay(day, month) {
            // Format the date for lookup in the events object
            const monthIndex = month - 1;
            const date = new Date(this.currentYear, monthIndex, day);
            const dateKey = date.toISOString().split('T')[0];
            
            this.selectedDay = {
                day,
                month,
                dateKey
            };
            
            this.updateSelectedDayEvents();
        },
        
        updateSelectedDayEvents() {
            if (!this.selectedDay) {
                this.selectedDayEvents = [];
                return;
            }
            
            // Get events for the selected date
            this.selectedDayEvents = this.events[this.selectedDay.dateKey] || [];
            
            // Filter events by selected calendars
            this.selectedDayEvents = this.selectedDayEvents.filter(event => 
                this.selectedCalendars.includes(event.calendarId)
            );
        },
        
        closeEventsPanel() {
            this.selectedDay = null;
            this.selectedDayEvents = [];
        },
        
        async saveNote(event) {
            if (!event.id || !event.note) return;
            
            try {
                const response = await fetch(`/api/events/${event.id}/note?calendar_id=${event.calendarId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        note: event.note
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`Failed to save note: ${response.statusText}`);
                }
                
                // Success message or notification could be shown here
                
            } catch (error) {
                console.error('Error saving note:', error);
                // Error message could be shown here
            }
        },
        
        // Helper functions
        formatSelectedDate() {
            if (!this.selectedDay) return '';
            
            const date = new Date(this.currentYear, this.selectedDay.month - 1, this.selectedDay.day);
            return date.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
        },
        
        formatEventTime(event) {
            if (!event.start) return '';
            
            // Handle multi-day events
            if (event.isMultiDay) {
                let eventTime = '';
                
                // All-day event
                if (event.start.date) {
                    // Parse the dates
                    const startDate = new Date(event.start.date);
                    let endDate;
                    
                    if (event.end && event.end.date) {
                        // Google Calendar stores end date as the day AFTER the last day
                        // Subtract one day to get the actual end date
                        endDate = new Date(event.end.date);
                        endDate.setDate(endDate.getDate() - 1);
                    } else {
                        endDate = startDate;
                    }
                    
                    // Format options
                    const dateOptions = { month: 'short', day: 'numeric' };
                    
                    if (event.isFirstDay) {
                        // This is the first day of the event
                        eventTime = `Multi-day: ${startDate.toLocaleDateString(undefined, dateOptions)} - ${endDate.toLocaleDateString(undefined, dateOptions)}`;
                    } else {
                        // Continuation of a multi-day event
                        eventTime = `Continues from ${startDate.toLocaleDateString(undefined, dateOptions)}`;
                    }
                    
                    return eventTime;
                } 
                
                // Timed multi-day event
                if (event.start.dateTime) {
                    const startDate = new Date(event.start.dateTime);
                    let endDate;
                    
                    if (event.end && event.end.dateTime) {
                        endDate = new Date(event.end.dateTime);
                    } else {
                        endDate = startDate;
                    }
                    
                    // Format options
                    const dateOptions = { month: 'short', day: 'numeric' };
                    const timeOptions = { hour: 'numeric', minute: '2-digit' };
                    
                    if (event.isFirstDay) {
                        // First day: show start time and date range
                        return `Starts: ${startDate.toLocaleTimeString(undefined, timeOptions)}, ${startDate.toLocaleDateString(undefined, dateOptions)} - ${endDate.toLocaleDateString(undefined, dateOptions)}`;
                    } else {
                        // Continuing days
                        return `Continues from ${startDate.toLocaleDateString(undefined, dateOptions)}`;
                    }
                }
            } else {
                // Regular single-day event
                // All-day event
                if (event.start.date) {
                    return 'All day';
                }
                
                // Timed event
                if (event.start.dateTime) {
                    const start = new Date(event.start.dateTime);
                    let end = '';
                    
                    if (event.end && event.end.dateTime) {
                        end = new Date(event.end.dateTime);
                    }
                    
                    const timeOptions = { hour: 'numeric', minute: '2-digit' };
                    
                    if (end) {
                        return `${start.toLocaleTimeString(undefined, timeOptions)} - ${end.toLocaleTimeString(undefined, timeOptions)}`;
                    } else {
                        return start.toLocaleTimeString(undefined, timeOptions);
                    }
                }
            }
            
            return '';
        },
        
        getEventColor(event) {
            const calendar = this.calendars.find(cal => cal.id === event.calendarId);
            return calendar ? calendar.backgroundColor : '#4285F4';
        },
        
        cleanDescription(description) {
            if (!description) return '';
            
            // Remove the note section from the displayed description
            return description.replace(/<!-- BIGASSCALENDAR_NOTE_START -->.*<!-- BIGASSCALENDAR_NOTE_END -->/gs, '').trim();
        }
    }));
});
class CalendarCanvas {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.resize();
        
        // Default transformation values
        this.scale = 1;
        this.translateX = 0;
        this.translateY = 0;
        
        // Dragging state
        this.isDragging = false;
        this.dragStartX = 0;
        this.dragStartY = 0;
        this.lastTranslateX = 0;
        this.lastTranslateY = 0;
        
        // Pinch-to-zoom state
        this.isPinching = false;
        this.initialPinchDistance = 0;
        this.initialScale = 1;
        
        // Day click callback
        this.onDayClick = null;
        
        // Add click event listener for cell selection
        this.canvas.addEventListener('click', this.handleClick.bind(this));
    }
    
    resize() {
        // Set canvas dimensions to match its display size
        const rect = this.canvas.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        
        // Recalculate cell dimensions
        this.calculateDimensions();
    }
    
    calculateDimensions() {
        // Calculate dimensions for cells based on canvas size
        const padding = 20;
        const availableWidth = this.canvas.width - (padding * 2);
        const availableHeight = this.canvas.height - (padding * 2);
        
        // Column widths (31 days + 1 for month labels)
        this.columnWidth = availableWidth / 32;
        
        // Row heights (12 months + 1 for day labels)
        this.rowHeight = availableHeight / 13;
        
        // Top-left corner of the grid
        this.gridX = padding;
        this.gridY = padding;
    }
    
    drawCalendar(year, events, calendars) {
        // Clear the canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Save the current context state
        this.ctx.save();
        
        // Apply transformations
        this.ctx.translate(this.translateX, this.translateY);
        this.ctx.scale(this.scale, this.scale);
        
        // Store calendar data
        this.year = year;
        this.events = events;
        this.calendars = calendars;
        
        // Draw calendar elements
        this.drawGrid();
        this.drawMonthLabels();
        this.drawDayLabels();
        this.drawEvents();
        
        // Restore the context
        this.ctx.restore();
    }
    
    drawGrid() {
        this.ctx.strokeStyle = '#e0e0e0';
        this.ctx.lineWidth = 1;
        
        const totalColumns = 32; // 31 days + month label column
        const totalRows = 13; // 12 months + day label row
        
        // Calculate grid dimensions
        const gridWidth = this.columnWidth * totalColumns;
        const gridHeight = this.rowHeight * totalRows;
        
        // Draw horizontal grid lines (separating months)
        for (let row = 0; row <= totalRows; row++) {
            const y = this.gridY + (row * this.rowHeight);
            
            this.ctx.beginPath();
            this.ctx.moveTo(this.gridX, y);
            this.ctx.lineTo(this.gridX + gridWidth, y);
            this.ctx.stroke();
        }
        
        // Draw vertical grid lines (separating days)
        for (let col = 0; col <= totalColumns; col++) {
            const x = this.gridX + (col * this.columnWidth);
            
            this.ctx.beginPath();
            this.ctx.moveTo(x, this.gridY);
            this.ctx.lineTo(x, this.gridY + gridHeight);
            this.ctx.stroke();
        }
    }
    
    drawMonthLabels() {
        const months = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ];
        
        this.ctx.font = '14px Arial';
        this.ctx.fillStyle = '#333';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        for (let i = 0; i < 12; i++) {
            const y = this.gridY + this.rowHeight + ((i + 0.5) * this.rowHeight);
            const x = this.gridX + (this.columnWidth / 2);
            
            this.ctx.fillText(months[i], x, y);
        }
    }
    
    drawDayLabels() {
        this.ctx.font = '14px Arial';
        this.ctx.fillStyle = '#333';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        for (let day = 1; day <= 31; day++) {
            const x = this.gridX + this.columnWidth + ((day - 0.5) * this.columnWidth);
            const y = this.gridY + (this.rowHeight / 2);
            
            this.ctx.fillText(day.toString(), x, y);
        }
    }
    
    drawEvents() {
        if (!this.events || Object.keys(this.events).length === 0) return;
        
        Object.entries(this.events).forEach(([dateKey, dayEvents]) => {
            if (!dayEvents || dayEvents.length === 0) return;
            
            // Parse the date to get day and month
            const date = new Date(dateKey);
            const day = date.getDate();
            const month = date.getMonth();
            
            // Calculate cell position
            const x = this.gridX + this.columnWidth + ((day - 1) * this.columnWidth);
            const y = this.gridY + this.rowHeight + (month * this.rowHeight);
            
            // Draw event indicators
            this.drawEventIndicator(x, y, dayEvents);
        });
    }
    
    drawEventIndicator(x, y, events) {
        // Sort events by calendar
        const eventsByCalendar = {};
        
        events.forEach(event => {
            if (!eventsByCalendar[event.calendarId]) {
                eventsByCalendar[event.calendarId] = [];
            }
            eventsByCalendar[event.calendarId].push(event);
        });
        
        // Get colors for each calendar
        const calendarColors = {};
        Object.keys(eventsByCalendar).forEach(calendarId => {
            const calendar = this.calendars.find(cal => cal.id === calendarId);
            calendarColors[calendarId] = calendar ? calendar.backgroundColor : '#4285F4';
        });
        
        // Draw indicators for each calendar's events
        const indicatorSize = Math.min(this.columnWidth, this.rowHeight) * 0.8;
        const cellCenterX = x + (this.columnWidth / 2);
        const cellCenterY = y + (this.rowHeight / 2);
        
        if (Object.keys(eventsByCalendar).length === 1) {
            // Single calendar: draw one colored circle
            const calendarId = Object.keys(eventsByCalendar)[0];
            const count = eventsByCalendar[calendarId].length;
            
            this.ctx.fillStyle = calendarColors[calendarId];
            this.ctx.beginPath();
            this.ctx.arc(cellCenterX, cellCenterY, indicatorSize / 2, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Add count text if there are multiple events
            if (count > 1) {
                this.ctx.fillStyle = 'white';
                this.ctx.font = '10px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(count.toString(), cellCenterX, cellCenterY);
            }
        } else {
            // Multiple calendars: draw pie segments
            const calendarIds = Object.keys(eventsByCalendar);
            const totalEvents = calendarIds.reduce((sum, id) => sum + eventsByCalendar[id].length, 0);
            
            let startAngle = 0;
            calendarIds.forEach(calendarId => {
                const count = eventsByCalendar[calendarId].length;
                const angle = (count / totalEvents) * (Math.PI * 2);
                
                this.ctx.fillStyle = calendarColors[calendarId];
                this.ctx.beginPath();
                this.ctx.moveTo(cellCenterX, cellCenterY);
                this.ctx.arc(cellCenterX, cellCenterY, indicatorSize / 2, startAngle, startAngle + angle);
                this.ctx.closePath();
                this.ctx.fill();
                
                startAngle += angle;
            });
            
            // Add total count text
            if (totalEvents > 1) {
                this.ctx.fillStyle = 'white';
                this.ctx.beginPath();
                this.ctx.arc(cellCenterX, cellCenterY, indicatorSize / 4, 0, Math.PI * 2);
                this.ctx.fill();
                
                this.ctx.fillStyle = '#333';
                this.ctx.font = '10px Arial';
                this.ctx.textAlign = 'center';
                this.ctx.textBaseline = 'middle';
                this.ctx.fillText(totalEvents.toString(), cellCenterX, cellCenterY);
            }
        }
    }
    
    handleClick(e) {
        if (this.isDragging) return;
        
        // Calculate mouse position relative to canvas
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;
        
        // Adjust for transformations
        const transformedX = (mouseX - this.translateX) / this.scale;
        const transformedY = (mouseY - this.translateY) / this.scale;
        
        // Check if the click is within the calendar grid
        if (transformedX < this.gridX || transformedY < this.gridY) return;
        
        // Calculate column and row
        const col = Math.floor((transformedX - this.gridX) / this.columnWidth);
        const row = Math.floor((transformedY - this.gridY) / this.rowHeight);
        
        // First column is for month labels, first row is for day labels
        if (col === 0 || row === 0) return;
        
        // Convert to day and month
        const day = col;
        const month = row;
        
        // Validate day and month
        if (day >= 1 && day <= 31 && month >= 1 && month <= 12) {
            // Check if this is a valid date (e.g., April doesn't have 31 days)
            const date = new Date(this.year, month - 1, day);
            if (date.getMonth() !== month - 1) return;
            
            // Trigger callback if defined
            if (this.onDayClick) {
                this.onDayClick(day, month);
            }
        }
    }
    
    // Pan (drag) methods
    startDrag(x, y) {
        this.isDragging = true;
        this.dragStartX = x;
        this.dragStartY = y;
        this.lastTranslateX = this.translateX;
        this.lastTranslateY = this.translateY;
    }
    
    drag(x, y) {
        if (!this.isDragging) return;
        
        const dx = x - this.dragStartX;
        const dy = y - this.dragStartY;
        
        this.translateX = this.lastTranslateX + dx;
        this.translateY = this.lastTranslateY + dy;
        
        this.drawCalendar(this.year, this.events, this.calendars);
    }
    
    endDrag() {
        this.isDragging = false;
    }
    
    // Zoom methods
    zoom(delta, x, y) {
        // Calculate zoom center (mouse position)
        const rect = this.canvas.getBoundingClientRect();
        const mouseX = x - rect.left;
        const mouseY = y - rect.top;
        
        // Calculate position before zoom
        const prevX = (mouseX - this.translateX) / this.scale;
        const prevY = (mouseY - this.translateY) / this.scale;
        
        // Update scale with limits
        const newScale = Math.max(0.5, Math.min(5, this.scale + delta));
        this.scale = newScale;
        
        // Calculate position after zoom
        const newX = (mouseX - this.translateX) / this.scale;
        const newY = (mouseY - this.translateY) / this.scale;
        
        // Adjust translation to keep the mouse position at the same point
        this.translateX += (newX - prevX) * this.scale;
        this.translateY += (newY - prevY) * this.scale;
        
        this.drawCalendar(this.year, this.events, this.calendars);
    }
    
    // Pinch-to-zoom methods for touch devices
    startPinch(touches) {
        if (touches.length !== 2) return;
        
        this.isPinching = true;
        this.initialPinchDistance = this.getPinchDistance(touches);
        this.initialScale = this.scale;
    }
    
    pinch(touches) {
        if (!this.isPinching || touches.length !== 2) return;
        
        const currentDistance = this.getPinchDistance(touches);
        const distanceRatio = currentDistance / this.initialPinchDistance;
        
        // Calculate pinch center
        const center = this.getPinchCenter(touches);
        
        // Calculate position before zoom
        const prevX = (center.x - this.translateX) / this.scale;
        const prevY = (center.y - this.translateY) / this.scale;
        
        // Update scale with limits
        const newScale = Math.max(0.5, Math.min(5, this.initialScale * distanceRatio));
        this.scale = newScale;
        
        // Calculate position after zoom
        const newX = (center.x - this.translateX) / this.scale;
        const newY = (center.y - this.translateY) / this.scale;
        
        // Adjust translation to keep the pinch center at the same point
        this.translateX += (newX - prevX) * this.scale;
        this.translateY += (newY - prevY) * this.scale;
        
        this.drawCalendar(this.year, this.events, this.calendars);
    }
    
    endPinch() {
        this.isPinching = false;
    }
    
    getPinchDistance(touches) {
        const dx = touches[0].clientX - touches[1].clientX;
        const dy = touches[0].clientY - touches[1].clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }
    
    getPinchCenter(touches) {
        return {
            x: (touches[0].clientX + touches[1].clientX) / 2,
            y: (touches[0].clientY + touches[1].clientY) / 2
        };
    }
}
#!/bin/bash
set -e  # Exit on error

# Script to set up and run the Big Ass Calendar application

# Configuration 
VENV_DIR="venv"
CONFIG_FILE="config.yaml"
GOOGLE_CLIENT_FILE="google_client.json"

# Colorized output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if file exists and create from sample if not
check_and_create_config() {
    local file="$1"
    local sample="$2"
    local desc="$3"
    
    if [ ! -f "$file" ]; then
        if [ -f "$sample" ]; then
            log_warning "$desc file not found! Creating from sample..."
            cp "$sample" "$file"
            log_info "Created $file from sample. You should edit it with your actual configuration."
        else
            log_error "$desc sample file not found at $sample!"
            return 1
        fi
    else
        log_info "Found $desc file at $file"
    fi
    
    return 0
}

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    log_info "Creating virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
    log_success "Virtual environment created"
else
    log_info "Using existing virtual environment"
fi

# Activate virtual environment
log_info "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
log_success "Virtual environment activated"

# Install dependencies
log_info "Installing dependencies..."
pip install -r requirements.txt
log_success "Dependencies installed"

# Check configuration files
check_and_create_config "$CONFIG_FILE" "config_sample.yaml" "Configuration" || exit 1
check_and_create_config "$GOOGLE_CLIENT_FILE" "google_client_sample.json" "Google client" || exit 1

# Check if we have a full Alpine.js library or just the placeholder
if [ -s "app/static/js/vendor/alpine.min.js" ]; then
    file_size=$(wc -c < "app/static/js/vendor/alpine.min.js")
    if [ "$file_size" -lt 5000 ]; then
        log_warning "Using simplified Alpine.js placeholder. For production use, download the full library:"
        log_info "curl -o app/static/js/vendor/alpine.min.js https://unpkg.com/alpinejs@3.13.3/dist/cdn.min.js"
    else
        log_info "Using full Alpine.js library"
    fi
fi

# Run the application
log_info "Starting Big Ass Calendar application..."
python run.py --config="$CONFIG_FILE" --google-client="$GOOGLE_CLIENT_FILE"

# If the application exits, deactivate the virtual environment
# Note: This typically won't be reached since the Flask application runs in the foreground
deactivate
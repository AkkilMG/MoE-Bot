#!/bin/bash

# Function to print messages in red
print_error() {
    echo -e "\033[0;31m$1\033[0m"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python is necessary to run this script. Please install Python."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip is necessary to run this script. Please install pip."
    exit 1
fi

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
else
    print_error "requirements.txt file not found."
    exit 1
fi

cls

# Run the Python application
if [ -f "app.py" ]; then
    python3 app.py
else
    print_error "app.py file not found."
    exit 1
fi

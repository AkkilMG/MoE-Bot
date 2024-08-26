# Function to print messages in red
function Print-Error {
    param ([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

# Check if Python is installed
if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Print-Error "Python is necessary to run this script. Please install Python."
    exit 1
}

# Check if pip is installed
if (-not (Get-Command pip3 -ErrorAction SilentlyContinue)) {
    Print-Error "pip is necessary to run this script. Please install pip."
    exit 1
}

# Install dependencies
if (Test-Path "requirements.txt") {
    pip3 install -r requirements.txt
} else {
    Print-Error "requirements.txt file not found."
    exit 1
}

cls

# Run the Python application
if (Test-Path "app.py") {
    python app.py
} else {
    Print-Error "app.py file not found."
    exit 1
}

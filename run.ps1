$ErrorActionPreference = "Stop"

# Set the working directory
Set-Location "C:\Users\Ali\SchoolManagementSystem"

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the application
python src/main.py

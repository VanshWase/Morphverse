#!/bin/bash

# Exit the script as soon as any command fails
set -e

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Collect static files (if your Flask app is using something like Flask-Assets)
echo "Collecting static files..."
flask collect  # If you are using Flask-Assets or similar tools

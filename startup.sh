#!/bin/bash

echo "Starting the application..."

# Navigate to the project directory
cd /home/site/wwwroot

# Activate the virtual environment
source antenv/bin/activate

# Export environment variables for Flask
export FLASK_APP=app_s.py
export FLASK_ENV=production

# Run the Flask application
flask run --host=0.0.0.0 --port=8000

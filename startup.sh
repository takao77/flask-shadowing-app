#!/bin/bash

echo "Starting the application..."
source antenv/bin/activate  # Activate the virtual environment
export FLASK_APP=app_s.py
export FLASK_ENV=production
gunicorn --bind 0.0.0.0:80 app_s:app


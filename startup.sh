#!/bin/bash

echo "Starting the application..."
source antenv/bin/activate
export FLASK_APP=app_s.py
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=80

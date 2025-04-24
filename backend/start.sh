#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
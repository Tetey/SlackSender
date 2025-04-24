#!/bin/bash

echo "Starting application setup..."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate
python manage.py migrate django_celery_beat

# Check if scheduler_scheduledmessage table exists
echo "Checking database tables..."
TABLE_EXISTS=$(python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
try:
    cursor.execute(\"SELECT 1 FROM information_schema.tables WHERE table_name='scheduler_scheduledmessage'\")
    result = cursor.fetchone()
    print(1 if result else 0)
except Exception as e:
    print(f'Error checking table: {e}')
    print(0)
")

if [ "$TABLE_EXISTS" -eq 0 ]; then
    echo "Table scheduler_scheduledmessage does not exist. Migrations may have failed."
    echo "Attempting to create table manually..."
    python manage.py migrate scheduler
fi

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT

# Note: Celery worker and beat processes are started separately by Railway
# based on the Procfile configuration:
# worker: celery -A core worker --loglevel=info
# beat: celery -A core beat --loglevel=info
# scheduler: python scheduler_runner.py
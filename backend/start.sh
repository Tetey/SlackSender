#!/bin/bash

echo "Starting application setup..."

# Check for Railway persistent storage
RAILWAY_DATA_DIR="${RAILWAY_VOLUME_MOUNT_PATH:-/data}"
echo "Checking for persistent storage at $RAILWAY_DATA_DIR"
if [ ! -d "$RAILWAY_DATA_DIR" ]; then
    echo "Creating persistent storage directory..."
    mkdir -p "$RAILWAY_DATA_DIR"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Check if scheduler_scheduledmessage table exists and has data
echo "Checking database tables..."
DB_PATH="${RAILWAY_DATA_DIR}/db.sqlite3"
if [ ! -f "$DB_PATH" ]; then
    DB_PATH="db.sqlite3"
fi

TABLE_COUNT=$(python -c "
import sqlite3
import os
db_path = '$DB_PATH'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='scheduler_scheduledmessage'\")
    result = cursor.fetchone()
    print(1 if result else 0)
    conn.close()
else:
    print(0)
")

if [ "$TABLE_COUNT" -eq 0 ]; then
    echo "Table scheduler_scheduledmessage does not exist. Migrations may have failed."
    echo "Attempting to create table manually..."
    python manage.py migrate scheduler
fi

# Start Django server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
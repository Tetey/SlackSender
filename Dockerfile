FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Copy project
COPY backend/ .

# Create entrypoint script
RUN echo '#!/bin/bash\n\
echo "Running migrations..."\n\
python3 manage.py migrate\n\
\n\
echo "Collecting static files..."\n\
python3 manage.py collectstatic --noinput\n\
\n\
echo "Starting application..."\n\
python3 -m gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Run the application
CMD ["/app/entrypoint.sh"]
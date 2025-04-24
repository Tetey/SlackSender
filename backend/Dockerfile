FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Run migrations and collect static files
RUN python3 manage.py collectstatic --noinput

# Start command
CMD python3 manage.py migrate && python3 -m gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
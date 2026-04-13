FROM python:3.9-slim

WORKDIR /app

# Install server dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

ENV FLASK_ENV=production

# Render injects $PORT at runtime; gunicorn reads it via shell form
CMD gunicorn --worker-class eventlet -w 1 --bind "0.0.0.0:${PORT:-10000}" server:app
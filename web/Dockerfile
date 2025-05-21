FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy web application code
COPY web/ /app/web/
COPY static/ /app/static/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=web/app.py
ENV FLASK_ENV=production

ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "/app/web/main.py"]
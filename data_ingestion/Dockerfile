FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY data_ingestion/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ingestion application code
COPY data_ingestion/ /app/data_ingestion/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "data_ingestion.api:app", "--host", "0.0.0.0", "--port", "8000"] 
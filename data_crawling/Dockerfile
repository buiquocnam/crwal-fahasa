FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY data_crawling/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy crawler application code
COPY data_crawling/ /app/data_crawling/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "data_crawling.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

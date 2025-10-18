# Use a lightweight official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files into the container
COPY . /app/

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Start Gunicorn server for Django
CMD ["gunicorn", "profile_api.wsgi:application", "--bind", "0.0.0.0:8000"]

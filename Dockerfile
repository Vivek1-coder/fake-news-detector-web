# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Set environment variable for Flask
ENV PORT 8080

# Command to run the app with Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

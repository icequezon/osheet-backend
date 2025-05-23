# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose port for the app
EXPOSE 5001

# Run the Flask app with Gunicornj
CMD ["gunicorn", "--chdir", "src", "--bind", "0.0.0.0:5001", "app:app", "--log-level ${DEBUG_LOG_LEVEL:-info}"]


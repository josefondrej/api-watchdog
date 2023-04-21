# Use a Python 3 runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory to /app
WORKDIR /app
ENV PYTHONPATH=/app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start python scripts /api_watchdog/frontend/app.py and /api_watchdog/monitoring/main.py in the background
CMD ["sh", "-c", "python /app/api_watchdog/monitoring/main.py & python /app/api_watchdog/frontend/app.py"]

# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory into the container
COPY src /app/src

# Set environment variable for Redis IP address
ENV REDIS_IP=your_redis_ip_address

# Expose port 5000 (or the port your Flask app is running on)
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "src/api.py"]

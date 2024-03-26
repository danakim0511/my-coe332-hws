# Use the official Python image as base
FROM python:3.9

# Set environment variables
ENV FLASK_APP=gene_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Set the working directory in the container
WORKDIR /app

# Install Flask and other dependencies
RUN pip install Flask==2.0.1

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]

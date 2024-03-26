# Use a Python base image
FROM python:3.9

# Set environment variables
ENV FLASK_APP=gene_api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run"]

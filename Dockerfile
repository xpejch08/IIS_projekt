# Use the official Python image as the base image
FROM python:3.8

LABEL authors="stepan"


# Copy your Flask app files into the container
COPY plannerBackend .

# Copy the requirements file into the container
COPY plannerBackend/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 5000

# Start your Flask app
CMD ["python", "backend.py"]

# Use the official Python 3.7 image as the base image
FROM python:3.7

# Set an environment variable to ensure Python prints to the console
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /usr/src/app/producer

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the producer.py script into the container
COPY producer.py .

# Define the command that will be executed when the container starts
CMD [ "python", "producer.py" ]
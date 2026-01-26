# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file and install the Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY ./src/ .

# Define the command to run your application (replace app.py with your main script)
ENTRYPOINT ["python", "-m", "src.api"]

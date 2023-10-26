# Use the official Airflow image as the base image
FROM apache/airflow:2.7.2

# Copy requirements.txt from the current directory to the image
COPY ./requirements.txt /requirements.txt

# Install additional requirements from requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
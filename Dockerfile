FROM python:3.9-slim-buster

# Install system dependencies
RUN apt-get update && apt-get install -y \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# ARG is a shell variable that can be set in the Dockerfile
ARG S3_BUCKET_EMPLOYEE_PHOTOS
ARG S3_REGION

# Update these lines
# ENV is an environment variable that can be set in the Dockerfile
ENV S3_BUCKET_EMPLOYEE_PHOTOS=${S3_BUCKET_EMPLOYEE_PHOTOS}
ENV S3_REGION=${S3_REGION}
ENV S3_BUCKET=${S3_BUCKET}


# Copy and install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application files
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Create upload folder
RUN mkdir -p /app/app/static/uploads

# Expose port 5000 for the Flask app
EXPOSE 5000

# Use the entrypoint script
CMD ["/bin/bash", "entrypoint.sh"]
#!/bin/bash

# Update the system
sudo yum update -y

# Install and configure Docker
sudo amazon-linux-extras install docker -y
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on

sudo docker run -d --name app -p 80:5000 \
  -e S3_BUCKET_EMPLOYEE_PHOTOS=${s3_bucket} \
  -e S3_REGION=${s3_region} \
  simonjan2/employee_management_flask_test:${app_version}

# Pull and run the Docker image
# Replace 'your-image:tag' with the actual image name and tag from Docker Hub
# sudo docker pull simonjan2/employee_management_flask_test:${app_version}
# sudo docker run -d -p 80:5000 simonjan2/employee_management_flask_test:${app_version}

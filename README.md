# Employee Management System

![Index](Readme/Index.png)

## Overview
This project is an Employee Management System built with Flask, featuring Docker containerization and Terraform for infrastructure deployment on AWS. It provides functionality for managing employees, handling tickets, and user authentication.

## Features
- User registration and authentication
- Employee management (add, view, delete)
- Ticket system for employee requests and issues
- Admin panel for user approval and ticket management
- S3 integration for employee profile picture storage
- Responsive design with particle.js background

## Tech Stack
- Backend: Flask
- Database: MariaDB
- Frontend: HTML, CSS, JavaScript (with particle.js)
- Containerization: Docker
- Infrastructure as Code: Terraform
- Cloud Provider: AWS
- CI/CD: GitHub Actions

## Project Structure
```
.
├── .github/workflows/      # GitHub Actions workflows
├── app/                    # Flask application
│   ├── static/             # Static assets (JS, CSS)
│   ├── templates/          # HTML templates
│   ├── __init__.py         # App initialization
│   ├── forms.py            # Form definitions
│   ├── models.py           # Database models
│   ├── routes.py           # Route definitions
│   └── s3_utils.py         # S3 utility functions
├── terraform/              # Terraform configuration files
├── .dockerignore
├── .gitignore
├── config.py               # Application configuration
├── Dockerfile              # Docker configuration
├── entrypoint.sh           # Docker entrypoint script
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Setup and Installation

### Local Development
1. Clone the repository:
   ```
   git clone <repository-url>
   cd employee-management-system
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   export FLASK_APP=app
   export FLASK_ENV=development
   export SECRET_KEY=your_secret_key
   export DATABASE_URL=mysql+pymysql://user:password@localhost/employee_management
   export S3_BUCKET=your_s3_bucket_name
   export AWS_ACCESS_KEY_ID=your_aws_access_key
   export AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   ```

5. Initialize the database:
   ```
   python init_db.py
   ```

6. Run the application:
   ```
   flask run
   ```

### Docker Deployment
1. Build the Docker image:
   ```
   docker build -t employee-management-system .
   ```

2. Run the container:
   ```
   docker run -d -p 5000:5000 \
     -e SECRET_KEY=your_secret_key \
     -e DATABASE_URL=mysql+pymysql://user:password@db_host/employee_management \
     -e S3_BUCKET=your_s3_bucket_name \
     -e AWS_ACCESS_KEY_ID=your_aws_access_key \
     -e AWS_SECRET_ACCESS_KEY=your_aws_secret_key \
     employee-management-system
   ```

### AWS Deployment with Terraform
1. Navigate to the terraform directory:
   ```
   cd terraform
   ```

2. Initialize Terraform:
   ```
   terraform init
   ```

3. Plan the infrastructure:
   ```
   terraform plan
   ```

4. Apply the configuration:
   ```
   terraform apply
   ```

5. After successful application, Terraform will output the application URL.

## CI/CD
This project uses GitHub Actions for continuous integration and deployment. Two workflows are defined:

1. `docker-workflow.yml`: Builds and pushes the Docker image on pushes to the main branch.
2. `terraform-workflow.yml`: Applies Terraform configuration to update the AWS infrastructure.

### GitHub Secrets
The following secrets are used in the GitHub Actions workflows and need to be set in your GitHub repository settings:

- `AWS_ACCESS_KEY_ID`: AWS access key for authentication
- `AWS_SECRET_ACCESS_KEY`: AWS secret key for authentication
- `AWS_REGION`: The AWS region where resources are deployed
- `BACKEND_REGION`: The AWS region for the Terraform backend
- `BUCKET_TF_STATE`: The S3 bucket name for storing Terraform state
- `DOCKERHUB_TOKEN`: DockerHub access token for pushing images
- `DOCKERHUB_USERNAME`: DockerHub username for pushing images
- `EC2_PRIVATE_KEY`: Private key for SSH access to EC2 instances
- `REPO_ACCESS_TOKEN`: GitHub repository access token
- `S3_BUCKET_EMPLOYEE_PHOTOS`: S3 bucket name for storing employee photos
- `S3_BUCKET_NAME`: General S3 bucket name (if different from employee photos)
- `S3_REGION`: AWS region for S3 buckets
- `TF_STATE_KEY`: Key for the Terraform state file in S3

Ensure these secrets are properly set before running the workflows.

## Environment Variables
In addition to the GitHub secrets, make sure to set the following environment variables in your deployment environment:

- `FLASK_APP=app`
- `FLASK_ENV=production` (use `development` for local setup)
- `SECRET_KEY=your_secret_key`
- `DATABASE_URL=mysql+pymysql://user:password@db_host/employee_management`

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
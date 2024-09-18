# Employee Management System

![Index2](Readme/Index2.png)

## Overview
This project is an Employee Management System built with Flask, featuring Docker containerization and Terraform for infrastructure deployment on AWS. It provides functionality for managing employees, handling tickets, and user authentication.

## Architecture
<!-- </details><details open><summary><strong>Click to collapse</strong></summary> -->
<details><summary>Click to expand</summary>
Below is a high-level architecture diagram of the Employee Management System:

```mermaid
graph TB
    subgraph "User Interaction"
        User["User/Browser"]
        AdminUser["Admin User"]
    end

    subgraph "AWS Cloud"
        VPC["VPC"]
        subgraph "Public Subnet 1"
            ALB["Application Load Balancer"]
            EC2_1["EC2 Instance 1<br>Docker Container"]
        end
        subgraph "Public Subnet 2"
            EC2_2["EC2 Instance 2<br>Docker Container"]
        end
        ASG["Auto Scaling Group"]
        S3["S3 Bucket<br>(Employee Photos)"]
        RDS["RDS MariaDB"]
        TFS3["S3 Bucket<br>(Terraform State)"]
        
        subgraph "EC2 Instance Components"
            Flask["Flask Application"]
            Gunicorn["Gunicorn WSGI Server"]
            DockerEngine["Docker Engine"]
        end
    end

    subgraph "External Services"
        GH["GitHub Repository"]
        DH["Docker Hub"]
    end

    subgraph "CI/CD Pipeline"
        GHA["GitHub Actions"]
        subgraph "Docker Workflow"
            DW1["Build Docker Image"]
            DW2["Push to Docker Hub"]
            DW3["Update Terraform Vars"]
        end
        subgraph "Terraform Workflow"
            TW1["Plan Infrastructure"]
            TW2["Apply Changes"]
            TW3["Deploy to EC2"]
        end
    end

    subgraph "Application Components"
        Routes["Routes (routes.py)"]
        Models["Models (models.py)"]
        Forms["Forms (forms.py)"]
        Templates["HTML Templates"]
        StaticFiles["Static Files (JS/CSS)"]
        S3Utils["S3 Utilities (s3_utils.py)"]
    end

    User -->|"HTTPS"| ALB
    AdminUser -->|"HTTPS"| ALB
    ALB -->|"HTTP"| EC2_1
    ALB -->|"HTTP"| EC2_2
    EC2_1 --> DockerEngine
    EC2_2 --> DockerEngine
    DockerEngine --> Flask
    Flask --> Gunicorn
    
    Flask --> Routes
    Routes --> Models
    Routes --> Forms
    Routes --> Templates
    Routes --> StaticFiles
    Routes --> S3Utils
    
    Models -->|"SQL Queries"| RDS
    S3Utils -->|"S3 API Calls"| S3
    
    ASG -->|"Manages"| EC2_1
    ASG -->|"Manages"| EC2_2
    
    GH -->|"Trigger"| GHA
    GHA --> DW1
    DW1 --> DW2
    DW2 --> DW3
    DW3 -->|"Trigger"| TW1
    TW1 --> TW2
    TW2 --> TW3
    TW3 -->|"Update"| EC2_1
    TW3 -->|"Update"| EC2_2
    DW2 -->|"Push Image"| DH
    TW2 -->|"Manage"| VPC
    TW2 -->|"Store State"| TFS3
    
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px;
    classDef external fill:#1EC9E8,stroke:#232F3E,stroke-width:2px;
    classDef cicd fill:#4CAF50,stroke:#232F3E,stroke-width:2px;
    classDef app fill:#7B68EE,stroke:#232F3E,stroke-width:2px;
    class ALB,EC2_1,EC2_2,ASG,S3,RDS,VPC,TFS3,DockerEngine aws;
    class GH,DH external;
    class GHA,DW1,DW2,DW3,TW1,TW2,TW3 cicd;
    class Flask,Gunicorn,Routes,Models,Forms,Templates,StaticFiles,S3Utils app;
```


This diagram illustrates the main components of the system and their interactions:

- **AWS Cloud**: Contains the core infrastructure including VPC, EC2 instances, Auto Scaling Group, Application Load Balancer, S3 buckets, and RDS database.
- **External Services**: GitHub for code hosting and Docker Hub for container image storage.
- **CI/CD Pipeline**: GitHub Actions for automating the build, test, and deployment processes.
- **User**: Represents end-users accessing the application through a web browser.

The arrows show the flow of data and interactions between different components, providing a clear overview of how the system operates.

Note: To view this diagram on GitHub, you may need to use a browser extension that renders Mermaid diagrams, or view the README through a Markdown viewer that supports Mermaid.
</details>

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

This project implements a Continuous Integration and Continuous Deployment (CI/CD) pipeline using GitHub Actions. The pipeline automates the process of building, testing, and deploying the application whenever changes are pushed to the main branch.

### Workflows

Two main workflows are defined in the `.github/workflows` directory:

1. `docker-workflow.yml`: Handles Docker image building and pushing
2. `terraform-workflow.yml`: Manages infrastructure updates using Terraform

#### Docker Workflow (`docker-workflow.yml`)

This workflow is triggered on pushes to the main branch and pull requests to the main branch.

Steps:
1. Checkout the repository
2. Set up Docker Buildx
3. Login to Docker Hub
4. Generate a new version number based on the current timestamp
5. Update the `app_version` in `terraform.tfvars`
6. Build and push the Docker image to Docker Hub
7. Commit and push the updated `terraform.tfvars` file
8. Trigger the Terraform workflow

Key Features:
- Automatically generates a unique version number for each build
- Updates the application version in Terraform variables
- Pushes the new Docker image to Docker Hub
- Triggers the Terraform workflow to update the infrastructure

#### Terraform Workflow (`terraform-workflow.yml`)

This workflow is triggered by the Docker workflow via a repository dispatch event.

Steps:
1. Checkout the repository
2. Set up Terraform
3. Create the `backend.tf` file for S3 backend configuration
4. Initialize Terraform
5. Validate and format Terraform files
6. Plan Terraform changes
7. Apply Terraform changes (if on main branch)
8. Retrieve information about the Auto Scaling Group
9. Get EC2 instance IPs
10. Create and execute a deployment script on EC2 instances
11. Output the application URL and deployment info

Key Features:
- Uses S3 as a backend for storing Terraform state
- Automatically applies infrastructure changes
- Retrieves information about deployed resources
- Executes a deployment script on EC2 instances to update the running application

### Deployment Process

1. Developer pushes changes to the main branch
2. Docker workflow builds and pushes a new Docker image
3. Docker workflow updates the `app_version` in Terraform variables
4. Docker workflow triggers the Terraform workflow
5. Terraform workflow updates the AWS infrastructure if needed
6. Terraform workflow deploys the new Docker image to EC2 instances
7. Application is updated with minimal downtime

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

### Environment Variables

In addition to the GitHub secrets, make sure to set the following environment variables in your deployment environment:

- `FLASK_APP=app`
- `FLASK_ENV=production` (use `development` for local setup)
- `SECRET_KEY=your_secret_key`
- `DATABASE_URL=mysql+pymysql://user:password@db_host/employee_management`

### Advantages of this CI/CD Setup

1. **Automation**: The entire process from code push to deployment is automated, reducing manual errors and saving time.
2. **Version Control**: Each deployment gets a unique version number, making it easy to track changes and rollback if needed.
3. **Infrastructure as Code**: Terraform ensures that infrastructure changes are version-controlled and repeatable.
4. **Scalability**: The use of Auto Scaling Groups allows the application to scale based on demand.
5. **Separation of Concerns**: Docker workflow handles application builds, while Terraform workflow manages infrastructure, allowing for independent scaling and management of each aspect.

### Potential Improvements

1. Implement automated testing in the Docker workflow before building the image.
2. Add a staging environment for testing changes before production deployment.
3. Implement blue-green deployments or canary releases for zero-downtime updates.
4. Set up monitoring and alerting for the CI/CD process and application health.

## Screenshots
![Employee](Readme/Employee.png)

![Tickets](Readme/Tickets.png)

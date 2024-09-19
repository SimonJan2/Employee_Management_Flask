import os

class Config:
    """
    Configuration class for the Flask application.
    This is how the application communicates with the database and other services.   
    """
    # Secret key for Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mysql+pymysql://user:password@100.28.95.161:3306/employee_management"
    # SQLAlchemy track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS Credentials for S3
    # S3_BUCKET is the name of the bucket where the employee photos will be stored
    S3_BUCKET = os.environ.get('S3_BUCKET_EMPLOYEE_PHOTOS')
    # S3_REGION is the region where the bucket is located
    S3_REGION = os.environ.get('S3_REGION')
    # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are the credentials for accessing the bucket
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY is the secret key for accessing the bucket
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    print(f"S3_BUCKET_EMPLOYEE_PHOTOS: {S3_BUCKET}")
    print(f"S3_REGION: {S3_REGION}")
    
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "mysql+pymysql://user:password@100.28.95.161:3306/employee_management"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # AWS Credentials for S3
    S3_BUCKET = os.environ.get('S3_BUCKET_EMPLOYEE_PHOTOS')
    S3_REGION = os.environ.get('S3_REGION')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    print(f"S3_BUCKET_EMPLOYEE_PHOTOS: {S3_BUCKET}")
    print(f"S3_REGION: {S3_REGION}")
    
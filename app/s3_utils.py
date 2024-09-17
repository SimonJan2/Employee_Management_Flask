import boto3
from botocore.exceptions import ClientError
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_s3_client():
    return boto3.client('s3', region_name=current_app.config['S3_REGION'])

def upload_file_to_s3(file_stream, filename):
    s3_client = get_s3_client()
    try:
        bucket = current_app.config['S3_BUCKET']
        logger.info(f"S3_BUCKET from config: {bucket}")
        logger.info(f"S3_REGION from config: {current_app.config['S3_REGION']}")
        
        if not bucket:
            logger.error("S3_BUCKET is not set in the configuration")
            return None

        logger.info(f"Attempting to upload file {filename} to bucket {bucket}")
        s3_client.upload_fileobj(file_stream, bucket, filename)
        return f"https://{bucket}.s3.{current_app.config['S3_REGION']}.amazonaws.com/{filename}"
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        return None
    except TypeError as e:
        logger.error(f"TypeError in upload_file_to_s3: {e}")
        return None
    
def delete_file_from_s3(filename):
    s3_client = get_s3_client()
    try:
        bucket = current_app.config['S3_BUCKET']
        s3_client.delete_object(Bucket=bucket, Key=filename)
        return True
    except ClientError as e:
        print(f"Error deleting file from S3: {e}")
        return False
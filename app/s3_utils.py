import boto3
from botocore.exceptions import ClientError
from flask import current_app
import logging

logger = logging.getLogger(__name__)

def get_s3_client():
    """
    Returns a boto3 client object for interacting with Amazon S3.

    Parameters:
        None

    Returns:
        boto3.client: An S3 client object.
    """
    return boto3.client('s3', region_name=current_app.config['S3_REGION'])

def upload_file_to_s3(file_stream, s3_key):
    """
    Uploads a file to an Amazon S3 bucket.

    Args:
        file_stream: A file-like object containing the file to be uploaded.
        s3_key (str): The S3 key (path) where the file will be stored.

    Returns:
        str: The URL of the uploaded file, or None if the upload fails.

    Raises:
        ClientError: If an error occurs while uploading the file to S3.
        TypeError: If a type error occurs while uploading the file to S3.
    """
    s3_client = get_s3_client()
    try:
        bucket = current_app.config['S3_BUCKET']
        logger.info(f"S3_BUCKET from config: {bucket}")
        logger.info(f"S3_REGION from config: {current_app.config['S3_REGION']}")
        
        if not bucket:
            logger.error("S3_BUCKET is not set in the configuration")
            return None

        logger.info(f"Attempting to upload file {s3_key} to bucket {bucket}")
        s3_client.upload_fileobj(file_stream, bucket, s3_key)
        return f"https://{bucket}.s3.{current_app.config['S3_REGION']}.amazonaws.com/{s3_key}"
    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        return None
    except TypeError as e:
        logger.error(f"TypeError in upload_file_to_s3: {e}")
        return None
    
def delete_file_from_s3(s3_key):
    """
    Deletes a file from an Amazon S3 bucket.

    Args:
        s3_key (str): The S3 key (path) of the file to be deleted.

    Returns:
        bool: True if the file is deleted successfully, False otherwise.

    Raises:
        ClientError: If an error occurs while deleting the file from S3.
    """
    s3_client = get_s3_client()
    try:
        bucket = current_app.config['S3_BUCKET']
        s3_client.delete_object(Bucket=bucket, Key=s3_key)
        return True
    except ClientError as e:
        logger.error(f"Error deleting file from S3: {e}")
        return False

def generate_presigned_url(s3_key, expiration=3600):
    """
    Generates a presigned URL for an S3 object.

    Args:
        s3_key (str): The S3 key (path) of the file.
        expiration (int): The number of seconds until the presigned URL expires.

    Returns:
        str: The presigned URL for the S3 object, or None if generation fails.

    Raises:
        ClientError: If an error occurs while generating the presigned URL.
    """
    s3_client = get_s3_client()
    try:
        bucket = current_app.config['S3_BUCKET']
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket,
                                                            'Key': s3_key},
                                                    ExpiresIn=expiration)
        return response
    except ClientError as e:
        logger.error(f"Error generating presigned URL: {e}")
        return None
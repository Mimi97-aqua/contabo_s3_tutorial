"""
Utitlity functions for the API
"""
import os
import mimetypes

import boto3
from botocore.config import Config


def generate_presigned_url(method:str, content_type:str, key:str=None):
    """
    Generates a presigned URL for uploading a file to Object Storage
    @param method: specifies the permission granted to the person accessing the URL
        - get_object is for download/view permission while
        - put_object is for upload
    @param key: unique key - can be anything
    @param content_tye: MIME type of the uploaded file

    returns: presigned URL for end-user
    """
    if method in ['put_object', 'get_object']:
        expiration = 3600  # 1 hour
    else:
        raise ValueError("Invalid method. Must be 'put_object' or 'get_object'.")

    s3 = boto3.resource(
        's3', # the servie name - it could be ec2, sqs and so on
        endpoint_url=os.environ.get('ENDPOINT_URL'), # used for bypassing the standard AWS Cloud for Contabo
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), # used in combination with with the secret key for login
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        config=Config(signature_version='s3v4') # protocol to sign web requests
    )

    """
    boto3.resource is more high-level and unlike boto3.client, it does not directly have the
    generate_presigned_url() method. Using meta.client.generate_preseigned_url() drops the
    resource down into a client in order to be able to 
    """
    url = s3.meta.client.generate_presigned_url(
        method=method,
        Params={
            'Bucket': os.environ.get('BUCKET_NAME'),
            'Key': key,
            'ContentType': content_type
        },
        ExpiresIn=expiration
    )

    return url


def check_size_and_type(file:object):
    """
    Validates that the uploaded file is a media file (audio, video, image) and checks that
    the maximum allowed file size is 5MB
    @param file: The uploaded file
    """
    ALLOWED_MIMETYPES = ('image/', 'video/', 'audio/')
    MAX_FILE_SIZE = 5 * 1024 * 1024
    mime_type, _ = mimetypes.guess_type(file, strict=True)

    file.seek(0, 2)
    file_length = file.tell()
    file.seek(0)

    is_valid_type = bool(mime_type and mime_type.startswith(ALLOWED_MIMETYPES))
    is_valid_size = bool(file_length <= MAX_FILE_SIZE)

    return is_valid_type, mime_type, is_valid_size

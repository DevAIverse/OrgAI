import os
import boto3
from botocore.client import Config

S3_ENDPOINT = os.getenv('S3_ENDPOINT')  # e.g., https://<ACCOUNT>.r2.cloudflarestorage.com
S3_REGION = os.getenv('S3_REGION') or 'auto'
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY') or os.getenv('S3_ACCESS_KEY_ID') or os.getenv('R2_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY') or os.getenv('R2_SECRET')

S3_BUCKET = os.getenv('S3_BUCKET') or 'orgai-docs'

def get_s3_client():
    if not S3_ENDPOINT:
        # default to boto3 without custom endpoint (works with real AWS if env configured)
        return boto3.client('s3')
    # S3-compatible (Cloudflare R2)
    return boto3.client('s3',
                        region_name=S3_REGION,
                        endpoint_url=S3_ENDPOINT,
                        aws_access_key_id=S3_ACCESS_KEY,
                        aws_secret_access_key=S3_SECRET_KEY,
                        config=Config(signature_version='s3v4'))

def presign_get(object_key, expires_in=300):
    s3 = get_s3_client()
    url = s3.generate_presigned_url('get_object',
                                    Params={'Bucket': S3_BUCKET, 'Key': object_key},
                                    ExpiresIn=expires_in)
    return url

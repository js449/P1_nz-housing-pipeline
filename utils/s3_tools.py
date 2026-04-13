import boto3
import os
from datetime import datetime


# This file contains utility functions for interacting with AWS S3.
# We have a generic upload function that can be used across different stages of the pipeline.

def upload_to_s3(local_file, bucket, folder):
    """
    Generic function to upload files to a specific S3 folder
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_name = os.path.basename(local_file)
    s3_path = f"{folder}/load_date={date_str}/{file_name}"
    
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_path)
        print(f"--- Successfully uploaded to S3: {s3_path} ---")
        return True
    except Exception as e:
        print(f"S3 Upload failed: {e}")
        return False
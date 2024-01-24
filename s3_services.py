
import os
import boto3
import pathlib
import json
from constants import ACCESS_KEY, SECRET_KEY, BUCKET_NAME




class S3:
    def __init__(self):
        self.s3 = boto3.client("s3",
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY)
    
    def upload_file(self, filename, bucket= BUCKET_NAME):
        local_filename = os.path.join(pathlib.Path(__file__).parent.resolve(), filename)
        print(filename)
        self.s3.upload_file(local_filename, bucket, filename)
        print('SUCCESS')
        return True
    
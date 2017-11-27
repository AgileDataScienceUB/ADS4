import sys
import boto3
import os

def get_s3_resource():
    return boto3.resource('s3')

def upload_file(filename, bucket, path=""):
    s3_resource = get_s3_resource()
    filename = filename.split("/")[-1]
    filename = filename.split("\\")[-1]
    s3_resource.Bucket(bucket).upload_file(filename, path + filename)

def download_file(key, bucket, local_path=None):
    if local_path is None:
        filename = key.split("/")[-1]
        filename = filename.split("\\")[-1]
        local_path = os.path.abspath(os.sep) + filename
    s3_resource = get_s3_resource()
    s3_resource.Bucket(bucket).download_file(key, local_path)

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 4:
            path = sys.argv[3]
        else:
            path=""

        upload_file(sys.argv[1], sys.argv[2], path=path)
    except Exception:
        print("Usage: \npython s3upload.py file bucket [path]")
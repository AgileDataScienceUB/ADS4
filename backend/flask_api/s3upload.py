import sys
import boto3

def get_s3_resource():
    return boto3.resource('s3')

def upload_file(filename, bucket, path=""):
    s3_resource = get_s3_resource()
    s3_resource.Bucket(bucket).upload_file(filename, path + filename)

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 4:
            path = sys.argv[3]
        else:
            path=""

        upload_file(sys.argv[1], sys.argv[2], path=path)
    except Exception:
        print(sys.exc_info()[2])
        print("Usage: \npython s3upload.py file bucket [path]")
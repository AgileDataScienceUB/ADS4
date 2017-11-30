import sys
import boto3
import os

def get_s3_client():
    return boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCES_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCES_KEY")
            )

def upload_file(filename, bucket, acl="public-read"):

    s3_client = get_s3_client()
    filename = filename.split("/")[-1]
    filename = filename.split("\\")[-1]
    file_object = open(filename, 'r')
    try:
        s3_client.upload_fileobj(
            file_object,
            bucket,
            filename,
            ExtraArgs={
                "ACL":acl,
                "ContentType":file_object.content_type
            }

        )
    except Exception as e:
        print("Something Happened:", e)
        return e
    
def download_file(key, bucket, local_path=None):
    if local_path is None:
        filename = key.split("/")[-1]
        filename = filename.split("\\")[-1]
        local_path = os.path.abspath(os.sep) + filename
    s3_resource = get_s3_client()
    s3_resource.Bucket(bucket).download_file(key, local_path)

if __name__ == '__main__':
    try:
        if len(sys.argv) >= 4:
            path = sys.argv[3]
        else:
            path=""

        upload_file(sys.argv[1], sys.argv[2])
    except Exception:
        print("Usage: \npython s3upload.py file bucket [path]")
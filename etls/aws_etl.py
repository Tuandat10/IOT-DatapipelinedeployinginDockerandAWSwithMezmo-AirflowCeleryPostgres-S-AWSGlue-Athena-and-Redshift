import s3fs
from utils.constants import BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION_NAME

def connect_to_s3():
    try:
        s3= s3fs.S3FileSystem(anon=False, key=AWS_ACCESS_KEY_ID, secret=AWS_SECRET_ACCESS_KEY)
        return s3
    except Exception as e:
        print(e)
def create_bucket_if_not_exists(s3, bucket_name):
    try:
        if not s3.exists(bucket_name):
            s3.mkdir(bucket_name)
            print(f"Bucket {bucket_name} created.")
        else:
            print(f"Bucket {bucket_name} already exists.")
    except Exception as e:
        print(f"Error creating bucket: {e}")
def upload_to_s3_syntax(s3,file_path,prefix,bucket,s3_filename):
    try:
        s3.put(file_path, f"{bucket}/{prefix}/{s3_filename}")
        print(f"File {s3_filename} uploaded to bucket {bucket}.")
    except Exception as e:
        print(f"Error uploading file: {e}")

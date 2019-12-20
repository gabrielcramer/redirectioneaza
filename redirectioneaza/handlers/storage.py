import boto3

from redirectioneaza.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, BUCKET_NAME


def save_file_to_s3(object_data, object_key):
    client = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    client.put_object(Body=object_data, Bucket=BUCKET_NAME, Key=object_key)


def retrieve_file_from_s3(object_key):
    client = boto3.client(
        's3',
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    return client.get_object(Bucket=BUCKET_NAME, Key=object_key)

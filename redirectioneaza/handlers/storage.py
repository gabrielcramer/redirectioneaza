
import boto3

from redirectioneaza import app

def save_file_to_s3(object_data, object_key):
    client = boto3.client(
        's3',
        region_name=app.config['AWS_REGION'],
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
    )

    client.put_object(ACL=app.config['BUCKET_OBJECT_ACL'], Body=object_data, Bucket=app.config['BUCKET_NAME'], Key=object_key)

    file_url = "https://s3.{0}.amazonaws.com/{1}{2}".format(app.config['AWS_REGION'], app.config['BUCKET_NAME'], object_key)

    return file_url

def retrieve_file_from_s3(object_key):
    client = boto3.client(
        's3',
        region_name=app.config['AWS_REGION'],
        aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],
    )

    return client.get_object(Bucket=app.config['BUCKET_NAME'], Key=object_key)

import boto3
import io
import json
import os
import pandas as pd


def get_s3_bucket():
    bucket_name = os.environ.get("AWS_S3_BUCKET")
    if bucket_name is None:
        raise ValueError(
            "AWS_S3_BUCKET env variable is empty"
        )

    s3_resource = boto3.resource("s3")
    return s3_resource.Bucket(bucket_name)


def load_s3_object(s3_object):
    s3_client = boto3.client("s3")
    with io.BytesIO() as buff:
        s3_client.download_fileobj(
            s3_object.Bucket().name,
            s3_object.key,
            buff
        )
        buff.seek(0)

        if s3_object.key.endswith("json"):
            return json.load(buff)
        elif s3_object.key.endswith("csv"):
            return pd.read_csv(buff, index_col=0)

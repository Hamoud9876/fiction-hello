import boto3
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def insert_into_bucket(bucket_name, table, content):
    s3_client = boto3.client("s3")

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    time = datetime.now().time().replace(microsecond=0)
    s3_key = f"{table}/{year}/{month}/{day}/{table}-{time}.csv"

    try:
        s3_client.put_object(Body=content, Bucket=bucket_name, Key=s3_key)
    except Exception as e:
        logger.error(f"Failed to upload ingested the content for {table} to S3: {e}")
        raise e

import logging
import boto3
from datetime import datetime, timezone
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def get_latest_file(directory: str, buck_name: str):
    """
    retrieves the latest file in the provided directory
    and turning it into df
    if no file can be found, an empty df will be returned.

    Args:
        directory: sirectory to be searched.
        ing_buck_name: the ingestion bucket where the raw
        file is stored


    Return:
        datafram contaning the content of the retrieved file
    """
    s3_client = boto3.client("s3")

    # date to store and ompare last modifed to
    output_file = datetime(2000, 1, 1, tzinfo=timezone.utc)

    # timestamp to retieve file dir based on
    timestamp = datetime.now()
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day

    prefix = f"{directory}/{year}/{month}/{day}"
    key = ""

    # retrieving all the files in the dir
    s3_response = s3_client.list_objects_v2(Bucket=buck_name, Prefix=prefix)

    # #checking if the bucket is empty
    if "Contents" not in s3_response or not s3_response["Contents"]:
        logger.info(f"No file was found for dir {directory}")
        return pd.DataFrame()

    # finding the most recent file
    for file in s3_response["Contents"]:
        if output_file < file["LastModified"]:
            output_file = file["LastModified"]
            key = file["Key"]

    # retrieving the file
    s3_file = s3_client.get_object(Bucket=buck_name, Key=key)

    # turning the file into a df
    df = pd.read_csv(s3_file["Body"], parse_dates=["created_at", "last_updated"])

    return df

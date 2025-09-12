import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime, timezone
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def read_parquet_file(bucket_name, timestamp, directory):
    """
    retrieves the latest parquet file in the provided directory.
    if no file can be found, an empty df will be returned.
    
    Args: 
        directory: sirectory to be searched.
        bucket_name: the procecssed bucket were the raw 
        file is stored
        timestamp: datetime input that makes up the key
    
    Return:
        datafram contaning the content of the retrieved file
    """

    #create boto3 client
    s3_client = boto3.client("s3")

    #date to store and ompare last modifed to
    output_file = datetime(2000,1,1, tzinfo=timezone.utc)

    #timestamp to retieve file dir based on
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day

    prefix = f"{directory}/{year}/{month}/{day}"
    key = ""


    #retrieving all the files in the dir
    s3_response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=prefix
    )


    # #checking if the bucket is empty
    if "Contents" not in s3_response or not s3_response["Contents"]:
        logger.info(f"No file was found in dir {directory}")
        return pd.DataFrame()


    #finding the most recent file
    for file in s3_response["Contents"]:
        if output_file < file["LastModified"]:
            output_file = file["LastModified"]
            key = file["Key"]


    #retrieving the file
    s3_file = s3_client.get_object(Bucket=bucket_name, Key=key)

    return pd.read_parquet(BytesIO(s3_file["Body"].read()), engine="pyarrow")
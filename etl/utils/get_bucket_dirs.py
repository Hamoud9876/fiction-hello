import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def get_bucket_dirs(bucket_name: str):
    """
    retrieves the diretory in the provided bucket
    name
    -----------------------------------------
    args: bucket_name: a sting represeting the
    S3 bucket name
    -----------------------------------------
    return: list contaning all the available directories
    """
    try:
        s3_client = boto3.client("s3")

        s3_respones = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Delimiter="/"
        )

        if "CommonPrefixes" not in s3_respones:
            return []

        directories = [directory["Prefix"].rstrip("/") 
                    for directory in s3_respones["CommonPrefixes"]]
    except Exception as e:
        logging.error(f"retrieving directory from {bucket_name} failed: {e}")
        raise e 

    logging.info(f"directories retrieved succussfully from {bucket_name}")
    
    return directories

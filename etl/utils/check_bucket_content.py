import boto3


def check_bucket_content(bucket_name: str):
    """
    checks if the S3 bucket is brand new or
    have been populated before
    -----------------------------------------
    args: bucket_name: a sting represeting the
    S3 bucket name
    -----------------------------------------
    return: int: 0 if the bucket is new and 1 if it was
    used before.
    """

    s3_client = boto3.client("s3")
    s3_response = s3_client.list_objects_v2(Bucket=bucket_name)

    if "Contents" in s3_response and len(s3_response["Contents"]) != 0:
        return True

    return False

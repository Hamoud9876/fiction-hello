from etl.utils.get_latest_file import get_latest_file
from moto import mock_aws
import boto3
import pytest
import os 
import pandas as pd


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3_client():
    with mock_aws():
        client = boto3.client("s3", region_name="eu-west-2")
        bucket_name = "test-bucket"
        client.create_bucket(Bucket=bucket_name,
                             CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})
        yield client, bucket_name

class TestIntegerationLatestFile:
    def test_returns_df(self, aws_credentials, s3_client):
        my_client, bucket_name = s3_client
        

        for i in range(2):
            s3_key = f"Hi/2025/8/23/{i}-{12-12-12}.csv"
            my_client.put_object(Body=b"content,hello", 
                                 Bucket=bucket_name, Key=s3_key)
            
        my_client.create_bucket(Bucket="processed-bucket",
                                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

        response = get_latest_file("Hi", bucket_name,"processed-bucket")

        assert isinstance(response, pd.DataFrame)
        

    def test_returns_correct_content(self, aws_credentials, s3_client):
        my_client, bucket_name = s3_client
        

        for i in range(2):
            s3_key = f"Hi/2025/8/23/{i}-{12-12-12}.csv"
            my_client.put_object(Body=b"content,hello", 
                                 Bucket=bucket_name, Key=s3_key)
            
        my_client.create_bucket(Bucket="processed-bucket",
                                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

        response = get_latest_file("Hi", bucket_name,"processed-bucket")
        
        assert "content" in response.columns
        assert "hello" in response.columns


    def test_handles_empty_bucket(self, aws_credentials, s3_client):
        my_client, bucket_name = s3_client
        

        for i in range(2):
            s3_key = f"Hi/2025/8/22/{i}-{12-12-12}.csv"
            my_client.put_object(Body=b"content,hello", 
                                 Bucket=bucket_name, Key=s3_key)
            
        my_client.create_bucket(Bucket="processed-bucket",
                                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"})

        response = get_latest_file("Hi", bucket_name,"processed-bucket")

        assert response == -1


        


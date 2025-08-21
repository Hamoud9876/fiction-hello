from etl.utils.get_bucket_dirs import get_bucket_dirs
import pytest
from moto import mock_aws
from unittest.mock import patch, MagicMock
import boto3
import os

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
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

class TestIntegerationGetBucketDir:
    def test_get_directories(self, s3_client):
        client, bucket_name = s3_client

        for i in range(2):
            s3_key = f"Hi+{i}/2020/1/sunday/{i}-{12-12-12}.csv"
            client.put_object(Body=b"content", Bucket=bucket_name, Key=s3_key)

        response = get_bucket_dirs(bucket_name)
        
        for i in range(len(response)):
            assert response[i] == f"Hi+{i}"


    @patch("etl.utils.get_bucket_dirs.boto3.client")
    def test_return_empty(self, mock_client):
        my_mock = MagicMock()
        my_mock.list_objects_v2.return_value = []
        mock_client.return_value = my_mock

        respones = get_bucket_dirs("test")

        assert respones == []


    @patch("etl.utils.get_bucket_dirs.boto3.client")    
    def test_handles_error(self, mock_client):
        my_mock = MagicMock()
        my_mock.list_objects_v2.side_effect = Exception("retrieving directory from test failed: error")
        mock_client.return_value = my_mock

        with pytest.raises(Exception) as e:
            get_bucket_dirs("test")

        assert "retrieving directory from test failed: error" in str(e.value)


from etl.utils.insert_into_bucket import insert_into_bucket
import pytest
import boto3
from moto import mock_aws
import os
from unittest.mock import patch


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


class TestInsertIntoBucket:
    @mock_aws
    @patch("etl.utils.insert_into_bucket.boto3.client")
    def test_puts_object(self, mock_boto, aws_credentials):
        bucket_name = "etl-ingestion-bucket-2025"
        table = "first_table"
        content = b"some content"

        mock_s3_client = mock_boto.return_value

        insert_into_bucket(bucket_name, table, content)

        mock_s3_client.put_object.assert_called_once()
        args, kwargs = mock_s3_client.put_object.call_args
        assert kwargs["bucket"] == bucket_name
        assert kwargs["Body"] == content
        assert kwargs["key"].startswith(table + "/")

    @mock_aws
    @patch("etl.utils.insert_into_bucket.boto3.client")
    def test_raises_error(self, mock_boto, aws_credentials):
        bucket_name = "etl-ingestion-bucket-2025"
        table = "first_table"
        content = b"some content"

        mock_s3 = mock_boto.return_value
        mock_s3.put_object.side_effect = Exception("exception raised")

        with pytest.raises(Exception) as e:
            insert_into_bucket(bucket_name, table, content)

        assert "exception raised" in str(e.value)

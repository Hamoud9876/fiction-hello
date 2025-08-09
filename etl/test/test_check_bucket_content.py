from etl.utils.check_bucket_content import check_bucket_content
import os
from moto import mock_aws
import boto3
from unittest.mock import patch, MagicMock
import pytest


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


class TestCheckBucketContent:
    @mock_aws
    @patch("etl.utils.check_bucket_content.boto3.client")
    def test_makes_call(self, mock_s3_client, aws_credentials):
        bucket_name = "hello"

        mock_s3_client.list_objects_v2.return_value = {"Contents": [{}, {}]}
        check_bucket_content(bucket_name)

        mock_s3_client.assert_called_once()

    @mock_aws
    @patch("etl.utils.check_bucket_content.boto3.client")
    def test_return_content(self, mock_s3_client, aws_credentials):
        bucket_name = "hello"

        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {"Contents": [{}, {}]}
        mock_s3_client.return_value = mock_s3

        result = check_bucket_content(bucket_name)
        assert result

    @mock_aws
    @patch("etl.utils.check_bucket_content.boto3.client")
    def test_return_no_content(self, mock_s3_client, aws_credentials):
        bucket_name = "hello"

        mock_s3 = MagicMock()
        mock_s3.list_objects_v2.return_value = {"Contents": []}
        mock_s3_client.return_value = mock_s3

        result = check_bucket_content(bucket_name)
        assert not result

        mock_s3.list_objects_v2.return_value = {}
        mock_s3_client.return_value = mock_s3

        result = check_bucket_content(bucket_name)
        assert not result

    @mock_aws
    @patch("etl.utils.check_bucket_content.boto3.client")
    def test_return_bool(self, mock_s3_client, aws_credentials):
        result = check_bucket_content("hello")
        assert isinstance(result, bool)

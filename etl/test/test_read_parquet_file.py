import pytest
import pandas as pd
from io import BytesIO
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from etl.utils.read_parquet_file import read_parquet_file  


def create_test_parquet():
    df = pd.DataFrame({
        "customer_id": [1, 2],
        "name": ["Alice", "Bob"]
    })
    buffer = BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)
    return buffer.getvalue()


@patch("etl.utils.read_parquet_file.boto3.client")
def test_read_parquet_file(mock_boto_client):
    # Setup
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3

    # Mock list_objects_v2 to return a single file
    mock_s3.list_objects_v2.return_value = {
        "Contents": [
            {
                "Key": "test/2025/9/12/file.parquet",
                "LastModified": datetime(2025, 9, 12, tzinfo=timezone.utc)
            }
        ]
    }

    # Mock get_object to return our in-memory Parquet file
    parquet_bytes = create_test_parquet()
    mock_s3.get_object.return_value = {
        "Body": BytesIO(parquet_bytes)
    }

    # Call function
    timestamp = datetime(2025, 9, 12)
    df = read_parquet_file("my-bucket", timestamp, "test")

    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["customer_id", "name"]
    assert df["customer_id"].tolist() == [1, 2]
    assert df["name"].tolist() == ["Alice", "Bob"]

    # Check boto3 calls
    mock_boto_client.assert_called_once_with("s3")
    mock_s3.list_objects_v2.assert_called_once()
    mock_s3.get_object.assert_called_once_with(
        Bucket="my-bucket",
        Key="test/2025/9/12/file.parquet"
    )

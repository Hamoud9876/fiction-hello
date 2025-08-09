from etl.src.lambda_ingestion.lambda_ingestion import ingest_data
from unittest.mock import patch, MagicMock
import os
import pytest


@pytest.fixture(scope="function")
def db_connection():
    with patch.dict(
        os.environ,
        {
            "DB_OLAP_USERNAME": "test_user",
            "DB_OLAP_PASSWORD": "test_pass",
            "DB_OLAP_DATABASE": "test_db",
            "DB_OLAP_HOST": "localhost",
            "DB_OLAP_PORT": "5432",
        },
        clear=False,
    ):
        yield


class TestIngestion:
    @patch("etl.src.lambda_ingestion.db_connection")
    def test_connection(self, db_connctoin):
        mock_connection = MagicMock()
        mock_connection.return_value = [["table_one"], ["table_two"]]
        db_connctoin.return_value = mock_connection

        ingest_data([], [])

        query_table_names = """
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE';"""

        mock_connection.run.assert_called_once_with(query_table_names)

    def test(self):
        ingest_data([], [])

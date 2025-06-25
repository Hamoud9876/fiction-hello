from unittest.mock import patch, MagicMock
from core.database.db_connection import db_connection, close_db
import os


class TestDBConnection:
    @patch.dict(
        os.environ,
        {
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_pass",
            "DB_DATABASE": "test_db",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
        },
    )
    @patch("core.database.db_connection.Connection")
    def test_db_connection(self, mock_connection):
        mock_conn_instance = MagicMock()
        mock_connection.return_value = mock_conn_instance

        conn = db_connection()

        mock_connection.assert_called_once_with(
            user="test_user",
            password="test_pass",
            database="test_db",
            host="localhost",
            port="5432",
        )
        assert conn == mock_conn_instance

    def test_close_db(self):
        mock_conn = MagicMock()
        close_db(mock_conn)
        mock_conn.close.assert_called_once()

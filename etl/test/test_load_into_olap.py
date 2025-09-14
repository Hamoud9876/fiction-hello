import pandas as pd
from unittest.mock import MagicMock, patch
from etl.utils.load_into_olap import insert_df_into_db
import pytest


@patch("etl.utils.load_into_olap.db_connection")
@patch("etl.utils.load_into_olap.close_db")
def test_insert_df_into_db(mock_close_db, mock_connection):
    mock_conn = MagicMock()
    mock_connection.return_value = mock_conn

    df = pd.DataFrame(
        [
            {"customer_id": 1, "name": "Alice", "email": "alice@example.com"},
            {"customer_id": 2, "name": "Bob", "email": "bob@example.com"},
        ]
    )

    insert_df_into_db(df, "dim_customers")

    mock_connection.assert_called_once()

    mock_close_db.assert_called_once_with(mock_conn)

    assert mock_conn.run.call_count == 2

    sql, kwargs = mock_conn.run.call_args[0][0], mock_conn.run.call_args[1]
    assert "ON CONFLICT (customer_id) DO UPDATE SET" in sql
    assert "name = EXCLUDED.name" in sql
    assert "email = EXCLUDED.email" in sql
    assert kwargs["customer_id"] == 2
    assert kwargs["name"] == "Bob"
    assert kwargs["email"] == "bob@example.com"

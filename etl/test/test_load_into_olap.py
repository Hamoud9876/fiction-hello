import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from etl.utils.load_into_olap import load_into_olap


@pytest.fixture
def sample_df():
    return pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})


def test_load_into_olap_success(sample_df):
    with patch.dict(
        "os.environ",
        {
            "DB_OLAP_HOST": "localhost",
            "DB_OLAP_PORT": "5432",
            "DB_OLAP_DATABASE": "test_db",
            "DB_OLAP_USERNAME": "user",
            "DB_OLAP_PASSWORD": "pass",
        },
    ), patch("etl.utils.load_into_olap.create_engine") as mock_create_engine, patch(
        "pandas.read_sql"
    ) as mock_read_sql:

        # Mock engine and connection
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.begin.return_value.__enter__.return_value = mock_conn

        # Simulate primary key query returning one PK column
        mock_conn.execute.return_value.fetchall.return_value = [("id",)]
        # Simulate empty existing table
        mock_read_sql.return_value = pd.DataFrame(columns=["id"])

        # Patch DataFrame.to_sql to avoid writing to DB
        with patch.object(pd.DataFrame, "to_sql", return_value=None) as mock_to_sql:
            result = load_into_olap(sample_df, "test_table")

        assert result == "Lambda finished successfully"
        mock_to_sql.assert_called_once()

import pytest
from unittest.mock import MagicMock, patch
from etl.utils.convert_to_csv import convert_to_csv


@pytest.fixture
def mock_conn():
    conn = MagicMock()
    return conn


@patch("etl.utils.convert_to_csv.insert_into_bucket")
def test_convert_into_csv_writes_csv(mock_insert, mock_conn):
    mock_conn.run.side_effect = [
        [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")],
        [("col1",), ("col2",)],
    ]

    table = "customers"
    bucket_name = "test-bucket"
    query = "SELECT * FROM customers;"

    convert_to_csv(table, bucket_name, mock_conn, query)

    args, kwargs = mock_insert.call_args
    assert args[0] == bucket_name
    assert args[1] == table

    csv_output = args[2]
    expected_csv = "col1,col2\r\nrow1_col1,row1_col2\r\nrow2_col1,row2_col2\r\n"
    assert csv_output == expected_csv


@patch("etl.utils.convert_to_csv.insert_into_bucket")
def test_convert_into_csv_empty_table(mock_insert, mock_conn):
    mock_conn.run.side_effect = [
        [],
        [("col1",), ("col2",)],
    ]

    table = "contracts"
    bucket_name = "test-bucket"
    query = "SELECT * FROM contracts;"

    convert_to_csv(table, bucket_name, mock_conn, query)

    args, _ = mock_insert.call_args
    csv_output = args[2]
    assert csv_output == "col1,col2\r\n"


@patch("etl.utils.convert_to_csv.insert_into_bucket")
def test_convert_into_csv_passes_correct_query(mock_insert, mock_conn):
    mock_conn.run.side_effect = [
        [("data1", "data2")],
        [("col1",), ("col2",)],
    ]

    table = "billing"
    bucket_name = "test-bucket"
    query = "SELECT * FROM billing;"

    convert_to_csv(table, bucket_name, mock_conn, query)

    first_call = mock_conn.run.call_args_list[0][0][0]
    assert first_call == query

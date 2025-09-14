from unittest.mock import patch, MagicMock
from etl.src.lambda_ingestion.lambda_ingestion import ingest_data

mock_event = {}
mock_context = {}


def test_ingest_data_first_time():
    with patch("etl.utils.convert_to_csv.convert_to_csv") as mock_convert_to_csv, patch(
        "etl.src.lambda_ingestion.lambda_ingestion.check_bucket_content"
    ) as mock_check_bucket, patch(
        "etl.src.lambda_ingestion.lambda_ingestion.db_connection"
    ) as mock_db_conn:

        mock_check_bucket.return_value = False
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn

        result = ingest_data(mock_event, mock_context)

        assert result == {"status": 200}
        assert mock_convert_to_csv.call_count == 28


def test_ref_tables_always_retrieved():
    with patch("etl.utils.convert_to_csv.convert_to_csv") as mock_convert_to_csv, patch(
        "etl.src.lambda_ingestion.lambda_ingestion.check_bucket_content"
    ) as mock_check_bucket, patch(
        "etl.src.lambda_ingestion.lambda_ingestion.db_connection"
    ) as mock_db_conn:

        mock_check_bucket.return_value = True
        mock_conn = MagicMock()
        mock_db_conn.return_value = mock_conn

        ingest_data(mock_event, mock_context)

        ref_tables = [
            "pronounce",
            "genders",
            "contract_types",
            "contracts_periods",
            "sims",
            "sims_validation",
            "devices",
            "devices_types",
            "address_type",
            "customers_status",
            "billing_status",
        ]

        # Filter convert_to_csv calls for ref_tables
        ref_calls = [
            call
            for call in mock_convert_to_csv.call_args_list
            if call[0][0] in ref_tables
        ]

        # Assert all ref tables were called exactly once
        assert len(ref_calls) == len(ref_tables)

        # Assert query for each ref table is SELECT * FROM {ref_table} (ignoring whitespace)
        for call in ref_calls:
            table_name = call[0][0]
            query = "".join(call[0][3].split())  # remove all whitespace
            expected = f"SELECT*FROM{table_name}"
            assert expected in query

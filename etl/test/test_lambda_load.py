from unittest.mock import patch, ANY
import pandas as pd
import pytest
from etl.src.lambda_load.lambda_load import lambda_load

@patch("etl.src.lambda_load.lambda_load.insert_df_into_db")
@patch("etl.src.lambda_load.lambda_load.read_parquet_file")
@patch("etl.src.lambda_load.lambda_load.get_bucket_dirs")
def test_lambda_load(mock_get_dirs, mock_read_parquet, mock_insert_db):
    mock_get_dirs.return_value = ["dim_customers", "dim_date"]

    df_customers = pd.DataFrame({"customer_id": [1], "name": ["Alice"]})
    df_date = pd.DataFrame({"date_id": [20250912], "day": [12]})

    mock_read_parquet.side_effect = [df_customers, df_date]

    event = {}
    context = {}
    result = lambda_load(event, context)
    assert result == {"status": 200}

    # Check insert_df_into_db calls
    assert mock_insert_db.call_count == 2
    args1, _ = mock_insert_db.call_args_list[0]
    args2, _ = mock_insert_db.call_args_list[1]

    pd.testing.assert_frame_equal(args1[0], df_customers)
    assert args1[1] == "dim_customers"

    pd.testing.assert_frame_equal(args2[0], df_date)
    assert args2[1] == "dim_date"

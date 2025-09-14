from unittest.mock import patch, ANY
import pandas as pd
from etl.src.lambda_load.lambda_load import lambda_load


@patch("etl.src.lambda_load.lambda_load.load_into_olap")
@patch("etl.src.lambda_load.lambda_load.read_parquet_file")
def test_lambda_load(mock_read_parquet, mock_insert_db):

    df_customers = pd.DataFrame({"customer_id": [1], "name": ["Alice"]})
    df_date = pd.DataFrame({"date_id": [20250912], "day": [12]})

    mock_read_parquet.side_effect = [
        df_date,
        df_customers,
        df_customers,
        df_customers,
        df_customers,
        df_customers,
        df_customers,
        df_customers,
        df_customers,
    ]

    event = {}
    context = {}
    result = lambda_load(event, context)
    assert result == {"status": 200}

    # Check insert_df_into_db calls
    assert mock_insert_db.call_count == 9

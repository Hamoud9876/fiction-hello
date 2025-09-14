from etl.src.lambda_transform.lambda_transform import lambda_transform
import pytest
import pandas as pd
from unittest.mock import patch


@pytest.fixture
def fake_event_context():
    return {}, {}


class TestLambdatransform:
    @patch("etl.src.lambda_transform.lambda_transform.insert_into_bucket")
    @patch("etl.src.lambda_transform.lambda_transform.get_bucket_dirs")
    @patch("etl.src.lambda_transform.lambda_transform.get_latest_file")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_customers")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_contract")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_location")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_date")
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_demo")
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_usage")
    @patch("etl.src.lambda_transform.lambda_transform.transform_billing")
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_contracts")
    def test_lambda_transform_success(
        self,
        mock_transform_customers_contracts,
        mock_transform_billing,
        mock_transform_customers_usage,
        mock_transform_customers_demo,
        mock_transform_dim_date,
        mock_transform_dim_location,
        mock_transform_dim_contract,
        mock_transform_dim_customers,
        mock_get_latest_file,
        mock_get_bucket_dirs,
        mock_insert_into_bucket,
    ):

        all_dirs = [
            "customers",
            "contracts",
            "billing",
            "genders",
            "address",
            "pronounce",
            "customers_status",
            "contracts_details_sims",
            "contracts_details_devices",
            "customers_usage",
            "customers_sims",
            "customers_address",
            "device_details",
            "sim_valid_history",
            "customer_status_history",
            "billing_status_history",
            "charge_rates",
            "personal_data",
            "contract_types",
            "contracts_periods",
            "sims",
            "sims_validation",
            "devices",
            "devices_types",
            "address_type",
            "billing_status",
            "customers_contracts",
            "contract_details",
            "contracts_periods",
        ]

        expected_tables = [
            "dim_customers",
            "dim_contract",
            "dim_location",
            "dim_date",
            "fact_customers_demographic",
            "fact_customers_usage",
            "fact_billing",
            "fact_customers_contracts",
        ]

        mock_get_bucket_dirs.return_value = all_dirs

        mock_get_latest_file.side_effect = lambda directory, *_: f"df_{directory}"

        mock_transform_dim_customers.return_value = pd.DataFrame({"a": [1, 2]})
        mock_transform_dim_contract.return_value = pd.DataFrame({"b": [3, 4]})
        mock_transform_dim_location.return_value = pd.DataFrame({"c": [5, 6]})
        mock_transform_dim_date.return_value = pd.DataFrame({"d": [7, 8]})
        mock_transform_customers_demo.return_value = pd.DataFrame({"e": [9, 10]})
        mock_transform_customers_usage.return_value = pd.DataFrame({"f": [11, 12]})
        mock_transform_billing.return_value = pd.DataFrame({"g": [13, 14]})
        mock_transform_customers_contracts.return_value = pd.DataFrame({"h": [15, 16]})
        mock_insert_into_bucket.return_value = True

        result = lambda_transform({}, {})

        assert result == {"status": 200}

        mock_get_bucket_dirs.assert_called_once()
        mock_transform_dim_customers.assert_called_once()
        mock_transform_dim_contract.assert_called_once()
        mock_transform_dim_location.assert_called_once()
        mock_transform_dim_date.assert_called_once()
        mock_transform_customers_demo.assert_called_once()
        mock_transform_customers_usage.assert_called_once()
        mock_transform_billing.assert_called_once()
        mock_transform_customers_contracts.assert_called_once()
        assert mock_insert_into_bucket.call_count == len(expected_tables)

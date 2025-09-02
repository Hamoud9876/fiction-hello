from etl.src.lambda_transform.lambda_transform import lambda_transform
import pytest
from unittest.mock import patch


@pytest.fixture
def fake_event_context():
    return {}, {} 

class TestLambdatransform:
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_contracts")
    @patch("etl.src.lambda_transform.lambda_transform.transform_billing")
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_usage")
    @patch("etl.src.lambda_transform.lambda_transform.transform_customers_demo")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_date")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_location")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_contract")
    @patch("etl.src.lambda_transform.lambda_transform.transform_dim_customers")
    @patch("etl.src.lambda_transform.lambda_transform.get_latest_file")
    @patch("etl.src.lambda_transform.lambda_transform.get_bucket_dirs")
    def test_lambda_transform_success(
        self,
        mock_get_bucket_dirs,
        mock_get_latest_file,
        mock_transform_dim_customers,
        mock_transform_dim_contract,
        mock_transform_dim_location,
        mock_transform_dim_date,
        mock_transform_customers_demo,
        mock_transform_customers_usage,
        mock_transform_billing,
        mock_transform_customers_contracts
    ):
        
        all_dirs = [
    "customers", "contracts", "billing", "genders", "address", "pronounce", "customers_status",
    "contracts_details_sims", "contracts_details_devices", "customers_usage", "customers_sims",
    "customers_address", "device_details", "sim_valid_history", "customer_status_history",
    "billing_status_history", "charge_rates", "personal_data", "contract_types",
    "contracts_periods", "sims", "sims_validation", "devices", "devices_types", "address_type",
    "billing_status", "customers_contracts", "contract_details", "contracts_periods"
]


        mock_get_bucket_dirs.return_value = all_dirs
        

        mock_get_latest_file.side_effect = lambda directory, *_: f"df_{directory}"


        mock_transform_dim_customers.return_value = "df_customers"
        mock_transform_dim_contract.return_value = "df_contract"
        mock_transform_dim_location.return_value = "df_location"
        mock_transform_dim_date.return_value = "df_date"
        mock_transform_customers_demo.return_value = "df_demo"
        mock_transform_customers_usage.return_value = "df_usage"
        mock_transform_billing.return_value = "df_billing"
        mock_transform_customers_contracts.return_value = "df_contracts"


        result = lambda_transform({}, {})


        assert result== {"status": 200}


        mock_get_bucket_dirs.assert_called_once()
        mock_transform_dim_customers.assert_called_once()
        mock_transform_dim_contract.assert_called_once()
        mock_transform_dim_location.assert_called_once()
        mock_transform_dim_date.assert_called_once()
        mock_transform_customers_demo.assert_called_once()
        mock_transform_customers_usage.assert_called_once()
        mock_transform_billing.assert_called_once()
        mock_transform_customers_contracts.assert_called_once()

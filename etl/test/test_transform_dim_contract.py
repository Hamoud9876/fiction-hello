from etl.utils.transform_dim_contract import transform_dim_contract
import pytest
import pandas as pd
from faker import Faker
import numpy as np
from datetime import timedelta, datetime

fake = Faker()


@pytest.fixture(scope="function")
def con_data():
    created_at = fake.date_time_between(start_date="-3y", end_date="now")
    last_updated = created_at + timedelta(days=np.random.randint(1, 500))

    contract_periods = pd.DataFrame(
        {
            "contract_period_id": range(1, 4),
            "period": [12, 24, 36],
            "created_at": created_at,
            "last_updated": last_updated,
        }
    )

    contract_types = pd.DataFrame(
        {
            "contract_type_id": range(1, 4),
            "contract_type": ["Mobile", "Broadband", "Bundle"],
            "created_at": created_at,
            "last_updated": last_updated,
        }
    )

    details_rows = []
    n = 5
    for i in range(n + 1):
        details_rows.append(
            {
                "contract_details_id": i,
                "contract_title": fake.catch_phrase(),
                "initial_price": round(np.random.uniform(10, 200), 2),
                "discount_percent": round(np.random.choice([0, 5, 10, 15, 20]), 1),
                "contract_period_id": np.random.choice(
                    contract_periods["contract_period_id"]
                ),
                "num_of_sims": np.random.randint(1, 5),
                "num_of_devices": np.random.randint(0, 3),
                "personal_data_id": 1,
                "start_date": created_at,
                "created_at": created_at,
                "last_updated": last_updated,
            }
        )

        contract_details = pd.DataFrame(details_rows)

    contracts_rows = []
    for i in range(n + 1):
        contracts_rows.append(
            {
                "contract_id": i,
                "contract_details_id": i,
                "contract_type_id": np.random.choice(
                    contract_types["contract_type_id"]
                ),
                "created_at": created_at,
                "last_updated": last_updated,
            }
        )

    contracts = pd.DataFrame(contracts_rows)

    yield contracts, contract_details, contract_periods, contract_types


class TestDimContract:
    def test_return_df(self, con_data):
        contracts, ontract_details, contract_periods, contract_types = con_data

        response = transform_dim_contract(
            contracts, ontract_details, contract_periods, contract_types
        )

        assert isinstance(response, pd.DataFrame)

    def test_correct_columns(self, con_data):
        contracts, ontract_details, contract_periods, contract_types = con_data

        response = transform_dim_contract(
            contracts, ontract_details, contract_periods, contract_types
        )

        assert "contract_title" in response
        assert "initial_price" in response
        assert "discount_percent" in response
        assert "num_of_sims" in response
        assert "num_of_devices" in response
        assert "personal_data_id" in response
        assert "contract_period" in response
        assert "contract_id" in response
        assert "contract_type" in response
        assert "effective_price" in response

        assert "contract_details_id" not in response
        assert "contract_type_id" not in response
        assert "contract_period_id" not in response

    def test_output_correct_data_type(self, con_data):
        contracts, ontract_details, contract_periods, contract_types = con_data

        response = transform_dim_contract(
            contracts, ontract_details, contract_periods, contract_types
        )

        assert isinstance(response["contract_title"].loc[0], str)
        assert isinstance(response["initial_price"].loc[0], np.floating)
        assert isinstance(response["discount_percent"].loc[0], np.integer)
        assert isinstance(response["num_of_sims"].loc[0], np.integer)
        assert isinstance(response["num_of_devices"].loc[0], np.integer)
        assert isinstance(response["personal_data_id"].loc[0], np.integer)
        assert isinstance(response["contract_period"].loc[0], np.integer)
        assert isinstance(response["contract_id"].loc[0], np.integer)
        assert isinstance(response["contract_type"].loc[0], str)
        assert isinstance(response["effective_price"].loc[0], np.floating)

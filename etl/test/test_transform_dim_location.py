from etl.utils.transform_dim_location import transform_dim_location
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import pytest

fake = Faker("en_GB")


# fixture to create address df
@pytest.fixture(scope="function")
def address():
    COUNTIES = [
        "Greater London",
        "West Midlands",
        "Greater Manchester",
        "Merseyside",
        "South Yorkshire",
        "West Yorkshire",
        "Tyne and Wear",
        "Hampshire",
        "Kent",
        "Essex",
        "Surrey",
        "Lancashire",
        "Devon",
        "Cornwall",
    ]

    start_date = fake.date_time_between(start_date="-5y", end_date="now")
    end_date = start_date + timedelta(days=np.random.randint(30, 1000))

    data = []

    n = 5
    for i in range(n):
        data.append(
            {
                "address_id": i,
                "first_line": fake.street_address(),
                "second_line": (
                    fake.secondary_address() if np.random.rand() > 0.5 else np.nan
                ),
                "city": fake.city(),
                "county": np.random.choice(COUNTIES),
                "post_code": fake.postcode(),
                "address_type_id": np.random.choice([1, 2]),
                "start_date": start_date,
                "end_date": end_date,
                "created_at": fake.date_time_between(
                    start_date=start_date, end_date=end_date
                ),
                "last_updated": datetime.now(),
            }
        )

    df = pd.DataFrame(data)

    yield df


# ficture to create address type df
@pytest.fixture(scope="function")
def address_type():
    df_address_type = pd.DataFrame(
        {"address_type_id": [1, 2], "address_type": ["Home", "Billing"]}
    )

    yield df_address_type


class TestTRansformDimLocation:
    def test_return_df(self, address, address_type):
        response = transform_dim_location(address, address_type)

        assert isinstance(response, pd.DataFrame)

    def test_transform_into_single_df(self, address, address_type):
        response = transform_dim_location(address, address_type)

        assert "location_id" in response
        assert "city" in response
        assert "county" in response
        assert "post_code" in response
        assert "address_type" in response
        assert "full_address" in response

        assert "address_type_id" not in response
        assert "first_line" not in response
        assert "second_line" not in response
        assert "start_date" not in response
        assert "end_date" not in response
        assert "created_at" not in response
        assert "last_updated" not in response

    def test_output_correct_data_type(self, address, address_type):
        response = transform_dim_location(address, address_type)

        assert isinstance(response["location_id"].loc[0], (int, np.integer))
        assert isinstance(response["city"].loc[0], str)
        assert isinstance(response["county"].loc[0], str)
        assert isinstance(response["post_code"].loc[0], str)
        assert isinstance(response["full_address"].loc[0], str)
        assert isinstance(response["address_type"].loc[0], str)

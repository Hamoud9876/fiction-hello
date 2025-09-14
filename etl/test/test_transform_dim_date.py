from etl.utils.transform_dim_date import transform_dim_date
import pandas as pd
import numpy as np
from faker import Faker
import pytest
from datetime import date


fake = Faker()


@pytest.fixture(scope="function")
def create_data():
    n = 10

    customers = pd.DataFrame(
        {
            "customer_id": [i + 1 for i in range(n)],
            "name": [fake.name() for _ in range(n)],
            "created_at": [
                fake.date_time_between(start_date="-5y", end_date="-1y")
                for _ in range(n)
            ],
            "last_updated": [
                fake.date_time_between(start_date="-1y", end_date="now")
                for _ in range(n)
            ],
            "birth_date": [
                fake.date_of_birth(minimum_age=18, maximum_age=70) for _ in range(n)
            ],
        }
    )

    contracts = pd.DataFrame(
        {
            "contract_id": [i + 1 for i in range(n)],
            "customer_id": np.random.randint(1, n + 1, size=n),
            "start_date": [
                fake.date_between(start_date="-3y", end_date="-6m") for _ in range(n)
            ],
            "end_date": [
                fake.date_between(start_date="-6m", end_date="now") for _ in range(n)
            ],
            "created_at": [
                fake.date_time_between(start_date="-3y", end_date="-2y")
                for _ in range(n)
            ],
            "last_updated": [
                fake.date_time_between(start_date="-1y", end_date="now")
                for _ in range(n)
            ],
        }
    )

    billing = pd.DataFrame(
        {
            "bill_id": [i + 1 for i in range(n)],
            "customer_id": np.random.randint(1, n + 1, size=n),
            "issue_date": [
                fake.date_time_between(start_date="-2y", end_date="now")
                for _ in range(n)
            ],
            "due_date": [
                fake.date_time_between(start_date="-1y", end_date="now")
                for _ in range(n)
            ],
            "completed_date": [
                (
                    fake.date_time_between(start_date="-1y", end_date="now")
                    if np.random.rand() > 0.3
                    else None
                )
                for _ in range(n)
            ],
            "created_at": [
                fake.date_time_between(start_date="-2y", end_date="-1y")
                for _ in range(n)
            ],
            "last_updated": [
                fake.date_time_between(start_date="-6m", end_date="now")
                for _ in range(n)
            ],
        }
    )

    devices = pd.DataFrame(
        {
            "device_id": [i + 1 for i in range(n)],
            "customer_id": np.random.randint(1, n + 1, size=n),
            "assigned_date": [
                fake.date_time_between(start_date="-3y", end_date="-1y")
                for _ in range(n)
            ],
            "returned_date": [
                (
                    fake.date_time_between(start_date="-1y", end_date="now")
                    if np.random.rand() > 0.5
                    else None
                )
                for _ in range(n)
            ],
            "created_at": [
                fake.date_time_between(start_date="-3y", end_date="-2y")
                for _ in range(n)
            ],
            "last_updated": [
                fake.date_time_between(start_date="-6m", end_date="now")
                for _ in range(n)
            ],
        }
    )

    usage = pd.DataFrame(
        {
            "usage_id": [i + 1 for i in range(n)],
            "customer_id": np.random.randint(1, n + 1, size=n),
            "start_date": [
                fake.date_time_between(start_date="-1y", end_date="-6m")
                for _ in range(n)
            ],
            "end_date": [
                fake.date_time_between(start_date="-6m", end_date="now")
                for _ in range(n)
            ],
            "created_at": [
                fake.date_time_between(start_date="-2y", end_date="-1y")
                for _ in range(n)
            ],
        }
    )

    return usage, devices, billing, contracts, customers


class TestTransformDimDate:
    def test_return_df(self, create_data):
        df1, df2, df3, df4, df5 = create_data

        response = transform_dim_date(df1=df1, df2=df2, df3=df3, df4=df4, df5=df5)

        assert isinstance(response, pd.DataFrame)

    def test_correct_columns(self, create_data):
        df1, df2, df3, df4, df5 = create_data

        response = transform_dim_date(df1=df1, df2=df2, df3=df3, df4=df4, df5=df5)

        assert "date_id" in response
        assert "day" in response
        assert "month" in response
        assert "year" in response
        assert "day_of_week" in response
        assert "day_name" in response
        assert "quarter" in response

    def test_output_correct_data_type(self, create_data):
        df1, df2, df3, df4, df5 = create_data

        response = transform_dim_date(df1=df1, df2=df2, df3=df3, df4=df4, df5=df5)

        assert isinstance(response["date_id"].loc[0], date)
        assert isinstance(response["day"].loc[0], np.integer)
        assert isinstance(response["month"].loc[0], np.integer)
        assert isinstance(response["year"].loc[0], np.integer)
        assert isinstance(response["day_of_week"].loc[0], np.integer)
        assert isinstance(response["day_name"].loc[0], str)
        assert isinstance(response["month_name"].loc[0], str)
        assert isinstance(response["quarter"].loc[0], np.integer)

    def test_empty_dfs(self):
        columns = ["created_at", "last_updated", "start_date", "end_date"]
        df1 = pd.DataFrame({col: pd.Series(dtype="datetime64[ns]") for col in columns})
        df2 = pd.DataFrame({col: pd.Series(dtype="datetime64[ns]") for col in columns})

        response = transform_dim_date(df1=df1, df2=df2)

        assert isinstance(response, pd.DataFrame)

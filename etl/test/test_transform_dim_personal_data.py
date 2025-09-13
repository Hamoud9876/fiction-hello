from etl.utils.transform_dim_personal_data import transform_personal_data
import pandas as pd
import numpy as np
import pytest
from dateutil.relativedelta import relativedelta
from datetime import date
from faker import Faker

fake = Faker()

@pytest.fixture(scope="function")
def create_data():
    start_date = fake.date_time_between(start_date="-5y", end_date="now")
    end_date = start_date + relativedelta(months=1)
    created_at = fake.date_time_between(start_date="-5y", end_date="now")
    last_updated = start_date + relativedelta(months=np.random.randint(1,500))


    n = 3
    personal_data = {
    "personal_data_id": [i + 1 for i in range(n)],
    "avail_cellular_data": [np.random.uniform(1.0, 150.0) for _ in range(n)],
    "avail_calls_time": [np.random.randint(1, 150) for _ in range(n)],
    "avail_roam_data": [np.random.uniform(1.0, 150.0) for _ in range(n)],
    "avail_roam_calls_time": [np.random.randint(1, 150) for _ in range(n)],
    "start_date": [start_date + relativedelta(months=i) for i in range(n)],
    "end_date": [end_date + relativedelta(months=i) for i in range(n)],
    "created_at": created_at,
    "last_updated": last_updated
    }

    df = pd.DataFrame(personal_data)

    #making the start and end date object type to match csv file
    df["start_date"] = df["start_date"].astype(object)
    df["end_date"] = df["end_date"].astype(object)

    yield  df


def test_return_df(create_data):
    df = create_data

    response = transform_personal_data(df)

    assert isinstance(response, pd.DataFrame)


def test_correct_columns(create_data):
    df = create_data

    response = transform_personal_data(df)


    assert "personal_data_id" in response
    assert "avail_calls_time" in response
    assert "avail_cellular_data" in response
    assert "avail_roam_data" in response
    assert "avail_roam_calls_time" in response
    assert "start_date" in response
    assert "end_date" in response


    assert "created_at" not in response
    assert "last_updated" not in response


def test_output_correct_data_type(create_data):
    df = create_data
    response = transform_personal_data(df)

    assert isinstance(response["personal_data_id"].loc[0], np.integer)
    assert isinstance(response["avail_calls_time"].loc[0], np.integer)
    assert isinstance(response["avail_cellular_data"].loc[0], np.floating)
    assert isinstance(response["avail_roam_data"].loc[0], np.floating)
    assert isinstance(response["avail_roam_calls_time"].loc[0], np.integer)
    assert isinstance(response["start_date"].loc[0], date)
    assert isinstance(response["end_date"].loc[0], date)



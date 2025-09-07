from etl.utils.transform_customers_usage import transform_customers_usage
import numpy as np
import pandas as pd
import pytest
from faker import Faker
from dateutil.relativedelta import relativedelta
from datetime import datetime, date


fake = Faker()


@pytest.fixture(scope=("function"))
def create_data():
    start_date = fake.date_time_between(start_date="-5y", end_date="now")
    end_date = start_date + relativedelta(months=1)


    n = 3
    customer_usage = {
    "customer_usage_id": [i + 1 for i in range(n)],
    "customer_id": [i + 1 for i in range(n)],
    "used_cellular_data": [np.random.uniform(1.0, 150.0) for _ in range(n)],
    "used_call_time": [np.random.randint(1, 150) for _ in range(n)],
    "used_roam_data": [np.random.uniform(1.0, 150.0) for _ in range(n)],
    "used_roam_call_time": [np.random.randint(1, 150) for _ in range(n)],
    "start_date": [start_date + relativedelta(months=i) for i in range(n)],
    "end_date": [end_date + relativedelta(months=i) for i in range(n)],
    "created_at": [fake.date_time_between(start_date="-5y", end_date="now")
                   for _ in range(n)],
    }

    customer_usage["last_updated"]= [
        i +relativedelta(days=np.random.randint(30, 1000))
        for i in customer_usage["created_at"]]
    
    df = pd.DataFrame(customer_usage)

    #making the start and end date object type to match csv file
    df["start_date"] = df["start_date"].astype(object)
    df["end_date"] = df["end_date"].astype(object)
    
    return df


class TestCustomersUsage:
    def test_return_df(self, create_data):
        df = create_data

        response = transform_customers_usage(df)

        assert isinstance(response,pd.DataFrame)

    def test_correct_datatype(self, create_data):
        df = create_data

        response = transform_customers_usage(df)

        assert isinstance(response["customer_id"].loc[0],np.integer)
        assert isinstance(response["used_cellular_data"].loc[0],np.floating) 
        assert isinstance(response["used_call_time"].loc[0], np.integer) 
        assert isinstance(response["used_roam_call_time"].loc[0], np.integer) 
        assert isinstance(response["used_roam_data"].loc[0], np.floating) 
        assert isinstance(response["start_date"].loc[0],date) 
        assert isinstance(response["end_date"].loc[0],date)
        assert isinstance(response["created_at"].loc[0], datetime)
        assert isinstance(response["last_updated"].loc[0], datetime)



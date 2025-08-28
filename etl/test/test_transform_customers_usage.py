from etl.utils.transform_customers_usage import transform_customers_usage
import numpy as np
import pandas as pd
import pytest
from faker import Faker
from dateutil.relativedelta import relativedelta


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
    "end_date": [end_date + relativedelta(months=i) for i in range(n)]
}
    
    return pd.DataFrame(customer_usage)


class TestCustomersUsage:
    def test_handle_empty_input(self, create_data):
        df = pd.DataFrame()

        response = transform_customers_usage(df)

        assert response is df


    def test_return_df(self, create_data):
        df = create_data

        response = transform_customers_usage(df)

        assert isinstance(response,pd.DataFrame)

    def test_correct_datatype(self, create_data):
        df = create_data

        response = transform_customers_usage(df)

        assert isinstance(response["customer_id"],) 
        assert isinstance(response["used_cellular_data"],) 
        assert isinstance(response["used_call_time"],) 
        assert isinstance(response["used_roam_call_time"],) 
        assert isinstance(response["used_roam_data"],) 
        assert isinstance(response["start_date"],) 
        assert isinstance(response["end_date"],) 


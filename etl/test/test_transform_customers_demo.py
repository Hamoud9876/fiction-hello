from etl.utils.transform_customers_demo import transform_customers_demo
import pandas as pd
import numpy as np
import pytest
from faker import Faker
from datetime import datetime, timedelta, date

fake = Faker()

@pytest.fixture(scope="function")
def create_data():
    n = 5
    data = {
    "customers_address_id": [i for i in range(n)],
    "customer_id": [i for i in range(n)],
    "address_id": [i for i in range(n)],
    "created_at": [fake.date_time_between(start_date="-5y", end_date="now")
                   for _ in range(n)],
    
}
    data["last_updated"]= [i +timedelta(days=np.random.randint(30, 1000))
                           for i in data["created_at"]]

    df_cust_address = pd.DataFrame(data)


    yield df_cust_address



class TestTransformCustomersDemo:
    def test_returns_df(self, create_data):
        df_cust_address = create_data

        response = transform_customers_demo(df_cust_address)
        
        assert isinstance(response, pd.DataFrame)


    def test_contains_currect_columns(self, create_data):
        df_cust_address = create_data

        response = transform_customers_demo(df_cust_address)

        assert "created_at" in response
        assert "last_updated" in response
        assert "customer_id" in response
        assert "address_id" in response

        assert "customers_address_id" not in response


    def test_correct_data_type(self, create_data):
        df_cust_address = create_data

        response = transform_customers_demo(df_cust_address)


        assert  isinstance(response["address_id"].loc[0], np.integer)
        assert  isinstance(response["created_at"].loc[0], datetime)
        assert  isinstance(response["last_updated"].loc[0], datetime)
        assert  isinstance(response["customer_id"].loc[0], np.integer)


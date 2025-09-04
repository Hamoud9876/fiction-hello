from etl.utils.transform_customers_demo import transform_customers_demo
import pandas as pd
import numpy as np
import pytest
from faker import Faker
from datetime import datetime, timedelta, date

fake = Faker()

@pytest.fixture(scope="function")
def create_data():
    start_date1 = fake.date_time_between(start_date="-5y", end_date="now")
    start_date2 = fake.date_time_between(start_date="-5y", end_date="now")
    end_date1 = start_date1 + timedelta(days=np.random.randint(30, 1000))
    end_date2 = start_date2 + timedelta(days=np.random.randint(30, 1000))

    df_location = pd.DataFrame({
        "location_id":[1,2],
        "city": ["Manchester", "Salford"],
        "county":["Greater Manchester", "Greater Manchester"],
        "post_code": ["P0 123", "PK6 1MM"],
        "start_date": [start_date1, start_date2],
        "end_date": [end_date1, end_date2],
        "created_at": [fake.date_time_between(start_date=start_date1, end_date=end_date1),
                       fake.date_time_between(start_date=start_date2, end_date=end_date2),],
        "last_updated": [start_date1, start_date2],
        "address_type": ["Home", "Home"],
        "full_address": ["32 house, flat 3", "44 house, flat 5"]
    })

    n = 2
    df_customers = pd.DataFrame({
        "customer_id": [i+1 for i in range(n)],  
        "first_name": [fake.first_name() for _ in range(n)],
        "middle_name": [fake.first_name() if np.random.uniform(0,1) > 0.4 else np.nan for _ in range(n)],
        "last_name": [fake.last_name() for _ in range(n)],
        "birthdate": [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(n)],
        "gender_id": [np.random.choice([1, 2, 3]) for _ in range(n)], 
        "pronounce_id": [np.random.choice([1, 2, 3]) for _ in range(n)],
        "join_date": [fake.date_time_this_decade() for _ in range(n)],
        "customer_status_id": [np.random.choice([1, 2, 3]) for _ in range(n)],
        "last_updated": [datetime.now() for _ in range(n)]
    })

    df_cust_address = pd.DataFrame()
    df_cust_address["customer_id"] = df_customers["customer_id"]
    df_cust_address["location_id"] = df_location["location_id"]


    yield df_location, df_cust_address



class TestTransformCustomersDemo:
    def test_returns_df(self, create_data):
        df_location, df_cust_address = create_data

        response = transform_customers_demo(df_location, df_cust_address)
        
        assert isinstance(response, pd.DataFrame)


    def test_contains_currect_columns(self, create_data):
        df_location, df_cust_address = create_data

        response = transform_customers_demo(df_location, df_cust_address)

        #columns left in
        assert "location_id" in response
        assert "start_date" in response
        assert "end_date" in response
        assert "created_at" in response
        assert "last_updated" in response
        assert "customer_id" in response

        #columns that were removed
        assert "city" not in response
        assert "county" not in response
        assert "post_code" not in response
        assert "address_type" not in response
        assert "full_address" not in response


    def test_correct_data_type(self, create_data):
        df_location, df_cust_address = create_data

        response = transform_customers_demo(df_location, df_cust_address)


        assert  isinstance(response["location_id"].loc[0], np.integer)
        assert  isinstance(response["start_date"].loc[0], datetime)
        assert  isinstance(response["end_date"].loc[0], datetime)
        assert  isinstance(response["created_at"].loc[0], datetime)
        assert  isinstance(response["last_updated"].loc[0], date)
        assert  isinstance(response["customer_id"].loc[0], np.integer)



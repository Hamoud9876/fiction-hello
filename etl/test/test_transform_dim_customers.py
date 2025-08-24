from etl.utils.transform_dim_customers import transform_dim_customers
import pandas as pd
from faker import Faker
from datetime import datetime, date
import numpy as np
import random
import pytest


fake = Faker()

@pytest.fixture(scope="function")
def create_custs():
    n = 50
    customers = {
        "customer_id": [i+1 for i in range(n)],  
        "first_name": [fake.first_name() for _ in range(n)],
        "middle_name": [fake.first_name() if random.uniform(0,1) > 0.4 else np.nan for _ in range(n)],
        "last_name": [fake.last_name() for _ in range(n)],
        "birthdate": [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(n)],
        "gender_id": [random.choice([1, 2, 3]) for _ in range(n)], 
        "pronounce_id": [random.choice([1, 2, 3]) for _ in range(n)],
        "join_date": [fake.date_time_this_decade() for _ in range(n)],
        "customer_status_id": [random.choice([1, 2, 3]) for _ in range(n)],
        "last_updated": [datetime.now() for _ in range(n)]
    }
    yield pd.DataFrame(customers)

@pytest.fixture(scope="function")
def gender():
    df = pd.DataFrame({
        "gender_id" : [1,2,3],
        "gender_title" : ["Male", "Female", "Non-Binary"]
    })

    yield df



@pytest.fixture(scope="function")
def pronounce():
    df = pd.DataFrame({
        "pronounce_id": [1,2,3],
        "pronounce_title": ["He/Him", "She/Her", "They/Them"]
    })

    yield df


@pytest.fixture(scope="function")
def cust_sts():
    df = pd.DataFrame({
        "customer_status_id": [1,2,3,4],
        "status": ["Active", "Inactive", "Blocked", "departed"]
    })

    yield df




class TestTransformDimCustomers:
    def test_return_df(self, create_custs, gender, pronounce,cust_sts):
        response = transform_dim_customers(create_custs, gender, pronounce, cust_sts)

        assert isinstance(response, pd.DataFrame)
        pd.set_option("display.max_columns", None)


    def test_transform_into_single_df(self, create_custs, gender, pronounce,cust_sts):
        response = transform_dim_customers(create_custs, gender, pronounce, cust_sts)

        assert "join_date" in response
        assert "full_name" in response
        assert "gender" in response
        assert "pronounce" in response
        assert "customer_status" in response
        assert "age" in response
        assert "age_group" in response
        assert "customer_id" in response

        assert "first_name" not in response
        assert "middle_name" not in response
        assert "last_name" not in response
        assert "last_updated" not in response
        assert "birthdate" not in response
        assert "gender_id" not in response
        assert "customer_status_id" not in response
        assert "pronounce_id" not in response


    def test_output_correct_data_type(self, create_custs, gender, pronounce,cust_sts):
        response = transform_dim_customers(create_custs, gender, pronounce, cust_sts)


        assert isinstance(response["join_date"].loc[0], date)
        assert isinstance(response["full_name"].loc[0], str)
        assert isinstance(response["gender"].loc[0], str)
        assert isinstance(response["pronounce"].loc[0], str)
        assert isinstance(response["customer_status"].loc[0], str)
        assert isinstance(response["age"].loc[0], (int, np.integer))
        assert isinstance(response["age_group"].loc[0], str)
        assert isinstance(response["customer_id"].loc[0], (int, np.integer))



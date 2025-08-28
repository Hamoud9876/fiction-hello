from etl.utils.transform_customers_contracts import transform_customers_contracts
import pandas as pd
import numpy as np
from faker import Faker
import pytest
from datetime import timedelta, date

fake = Faker()



@pytest.fixture(scope="function")
def create_data():
    contract_periods = pd.DataFrame({
        "contract_period_id": range(1, 4),
        "period": [12, 24, 36]
    })


    details_rows = []
    n = 5
    for i in range(n + 1):
        created_at = fake.date_time_between(start_date="-3y", end_date="now")
        last_updated = created_at + timedelta(days=np.random.randint(1, 500))
        
        details_rows.append({
            "contract_details_id": i,
            "contract_title": fake.catch_phrase(),
            "initial_price": round(np.random.uniform(10, 200), 2),
            "discount_percent": round(np.random.choice([0, 5, 10, 15, 20]), 1),
            "contract_period_id": np.random.choice(contract_periods["contract_period_id"]),
            "num_of_sims": np.random.randint(1, 5),
            "num_of_devices": np.random.randint(0, 3),
            "personal_data_id": np.random.randint(1, 50),
            "created_at": created_at,
            "last_updated": last_updated
        })

    contract_details = pd.DataFrame(details_rows)


    contracts_rows = []
    for i in range(n + 1):
        created_at = contract_details.iloc[i]["created_at"]
        last_updated = contract_details.iloc[i]["last_updated"]
        
        contracts_rows.append({
            "contract_id": i,
            "contract_details_id": contract_details.iloc[i]["contract_details_id"],
            "contract_type_id": np.random.choice([1,2,3]),
            "created_at": created_at,
            "last_updated": last_updated
        })

    contracts = pd.DataFrame(contracts_rows)

  
    customers_contracts_rows = []
    for i in range(n + 1):
        customers_contracts_rows.append({
            "customer_contract_id": i,
            "customer_id": np.random.randint(1, 50),
            "contract_id": contracts.iloc[i]["contract_id"]
        })

    customers_contracts = pd.DataFrame(customers_contracts_rows)

    return contract_periods, contract_details, contracts, customers_contracts



class TestTransformCustomersContracts:
    def test_returns_df(self, create_data):
        df_periods, df_con_detail, df_con, df_cust_con = create_data
        response = transform_customers_contracts(df_cust_con, df_con, df_con_detail,df_periods)

        assert isinstance(response,pd.DataFrame)


    def test_contains_currect_columns(self, create_data):
        df_periods, df_con_detail, df_con, df_cust_con = create_data
        response = transform_customers_contracts(df_cust_con, df_con, df_con_detail,df_periods)

        
        assert "customer_id" in response
        assert "contract_id" in response
        assert "created_at" in response
        assert "last_updated" in response
        assert "period" in response
        assert "start_date" in response
        assert "end_date" in response
        assert "is_active" in response



        assert "customer_contract_id" not in response
        



    def test_correct_data_type(self, create_data):
        df_periods, df_con_detail, df_con, df_cust_con = create_data
        response = transform_customers_contracts(df_cust_con, df_con, df_con_detail,df_periods)


        assert isinstance(response["customer_id"].loc[0], np.integer)
        assert isinstance(response["contract_id"].loc[0], np.integer )
        assert isinstance(response["created_at"].loc[0], date)
        assert isinstance(response["last_updated"].loc[0],date)
        assert isinstance(response["period"].loc[0], np.integer)
        assert isinstance(response["start_date"].loc[0], date)
        assert isinstance(response["end_date"].loc[0], date)
        assert isinstance(response["is_active"].loc[0], np.bool)


    def test_handles_empty_input(self, create_data):
        #df_con empty
        df_periods, df_con_detail, df_con, df_cust_con = create_data
        df_con = pd.DataFrame()
        response = transform_customers_contracts(df_cust_con, df_con, df_con_detail,df_periods)

        assert response is df_cust_con

        #df_cust_con empty
        df_periods, df_con_detail, df_con, df_cust_con = create_data
        df_cust_con = pd.DataFrame()

        response = transform_customers_contracts(df_cust_con, df_con, df_con_detail,df_periods)

        assert response is df_cust_con



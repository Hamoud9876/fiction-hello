from etl.utils.transform_billing import transform_billing
import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta, date, datetime
import pytest



fake = Faker()


@pytest.fixture(scope="function")
def create_data():
    n = 5  

    billing = pd.DataFrame({
        "bill_id": range(1, n+1),
        "customer_id": np.random.randint(1, 10, size=n),
        "contract_id": np.random.randint(1, 10, size=n),
        "amount": np.round(np.random.uniform(50.0, 1000.0, size=n), 2),
        "bill_status_id": np.random.randint(1, 3, size=n),
        "issue_date": [fake.date_time_between(start_date="-2y", end_date="now") for _ in range(n)],
    })


    billing["due_date"] = billing["issue_date"] + pd.to_timedelta(7, unit="d")


    billing["completed_date"] = [
        date + timedelta(days=np.random.randint(0, 31)) if np.random.rand() > 0.3 else None
        for date in billing["issue_date"]]

    billing["created_at"] = [fake.date_time_between(start_date="-2y", end_date="now") for _ in range(n)]
    billing["last_updated"] = billing["created_at"] + pd.to_timedelta(np.random.randint(0, 365, size=n), unit='d')


    billing_status = pd.DataFrame({
        "bill_status_id": [1,2],
        "status": ["paid", "unpaid"]
    })
    billing_status["created_at"] = [fake.date_time_between(start_date="-2y", end_date="now") for _ in range(2)]
    billing_status["last_updated"] = billing["created_at"] + pd.to_timedelta(np.random.randint(0, 365, size=n), unit='d')

    

    yield billing, billing_status

class TestTransofromBilling:
    def test_return_df(self, create_data):
        df_billing, df_status = create_data

        response = transform_billing(df_billing,df_status)

        assert isinstance(response,pd.DataFrame)

    
    def test_contains_currect_columns(self, create_data):
        df_billing, df_status = create_data

        response = transform_billing(df_billing,df_status)

        # assert "bill_id" in response
        assert "customer_id" in response
        assert "contract_id" in response
        assert "issue_date" in response
        assert "due_date" in response
        assert "complete_date" in response
        assert "bill_status" in response
        assert "amount_billed" in response
        assert "amount_paid" in response
        assert "is_paid" in response
        assert "days_overdue" in response


        assert "bill_status_id" not in response
        assert "amount" not in response



    def test_output_correct_data_type(self, create_data):
        df_billing, df_status = create_data

        response = transform_billing(df_billing,df_status)

        # assert isinstance(response["bill_id"].loc[0],np.integer)
        assert isinstance(response["customer_id"].loc[0],np.integer)
        assert isinstance(response["contract_id"].loc[0],np.integer)
        assert isinstance(response["issue_date"].loc[0], date)
        assert isinstance(response["due_date"].loc[0],date)
        assert isinstance(response["complete_date"].loc[0],date)
        assert isinstance(response["bill_status"].loc[0], str)
        assert isinstance(response["amount_billed"].loc[0],np.floating)
        assert isinstance(response["amount_paid"].loc[0],np.floating)
        assert isinstance(response["is_paid"].loc[0], np.bool)
        assert isinstance(response["days_overdue"].loc[0],np.integer)
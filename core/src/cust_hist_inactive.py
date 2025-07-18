from datetime import date
from faker import Faker
import inspect
from core.exceptions.invalid_input_exception import InvalidInput


def cust_hist_inactive(customers_status: list, join_date: date):
    """
    creates one recored for an inactive customer
    -----------------------------------------
    args: "customers_status" represent the available status
    any custoemr can have

    "join_date" the date the customer join the company
    -----------------------------------------
    return: a dict containing the most recent status
    along with the status history
    """
    if not isinstance(customers_status, list):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': list")
    if not isinstance(join_date, date):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': date")

    fake = Faker()

    return {
        "customer_status": customers_status[1],
        "cust_sts_hist": [
            {
                "customer_status": customers_status[0],
                "change_date": join_date,
            },
            {
                "customer_status": customers_status[1],
                "change_date": fake.date_between(join_date, "now"),
            },
        ],
    }

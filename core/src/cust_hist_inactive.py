from datetime import date
from faker import Faker


def cust_hist_inactive(customers_status: list, join_date: date, cust_id: int):
    """
    creates one recored for an inactive customer
    -----------------------------------------
    args: "customers_status" represent the available status
    any custoemr can have

    "join_date" the date the customer join the company

    "cust_id" customer_id
    -----------------------------------------
    return: a dict containing the most recent status
    along with the status history
    """
    if not isinstance(customers_status, list):
        return "Not a valid customer status input"
    if not isinstance(join_date, date):
        return "Not a valid date input"
    if not isinstance(cust_id, int):
        return "Not a valid customer id"

    fake = Faker()

    return {
        "customer_status": customers_status[1],
        "cust_sts_hist": [
            {
                "customer_status": customers_status[0],
                "customer_id": cust_id,
                "change_date": join_date,
            },
            {
                "customer_status": customers_status[1],
                "customer_id": cust_id,
                "change_date": fake.date_between(join_date, "now"),
            },
        ],
    }

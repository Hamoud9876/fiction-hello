from core.data.data import customers_status
from random import randint
from core.src.cust_hist_active import cust_hist_active
from core.src.cust_hist_inactive import cust_hist_inactive
from core.src.cust_hist_long_changes import cust_hist_long_changes
from core.exceptions.invalid_input_exception import InvalidInput
import inspect
from datetime import date


def customers_status_data(join_date: date):
    """
    creates customer status history and current status
    -----------------------------------------
    args: "join_date" represent the date of which
    the customer joined the orgnization
    -----------------------------------------
    return: a dict containing the most recent status
    along with the status history if exists
    """

    if not isinstance(join_date, date):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': date")

    rand_num = randint(0, 9)
    # customer active since joining
    if rand_num < 3:
        return cust_hist_active(customers_status, join_date)

    # customer not active anynore
    elif rand_num == 3:
        return cust_hist_inactive(customers_status, join_date)

    # complecated history of multiple changes
    else:
        return cust_hist_long_changes(customers_status, join_date)

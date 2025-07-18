from datetime import date, timedelta
from faker import Faker
from random import randint, sample
from core.utils.days_between import days_between
import inspect
from core.exceptions.invalid_input_exception import InvalidInput


def cust_hist_long_changes(cust_status: list, join_date: date):
    """
    creates one recored for a customer with one to  many changes
    -----------------------------------------
    args: "customers_status" represent the available status
    any custoemr can have

    "join_date" the date the customer join the company
    -----------------------------------------
    return: a dict containing the most recent status
    along with the status history
    """

    if not isinstance(cust_status, list):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': list")
    if not isinstance(join_date, date):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in function '{func_name}': date")

    # customers always active when created
    hist_lst = [
        {
            "customer_status": cust_status[0],
            "change_date": join_date,
        },
    ]
    previous_status = "Active"

    fake = Faker()

    change_date = fake.date_between(start_date=join_date, end_date="now")

    days_diff = days_between(join_date, change_date)

    # less than 3 years
    if days_diff < 1095:
        # deciding how many changes
        # 30% to have a change in status
        if randint(0, 9) > 3:
            hist_lst.append(
                {
                    "customer_status": cust_status[randint(1, 2)],
                    "change_date": change_date,
                },
            )
    else:
        num_periods = randint(2, 3)
        change_points = sorted(sample(range(50, days_diff), num_periods - 1))

        periods = (
            [change_points[0]]
            + [
                change_points[i] - change_points[i - 1]
                for i in range(1, len(change_points))
            ]
            + [days_diff - change_points[-1]]
        )

        effective_date = join_date + timedelta(days=periods[0])

        for i in range(num_periods):
            hist_lst.append(
                {
                    "customer_status": (
                        cust_status[randint(1, 2)]
                        if previous_status == "Active"
                        else cust_status[0]
                    ),
                    "change_date": effective_date,
                },
            )
            if i < num_periods - 1:
                effective_date = effective_date + timedelta(days=periods[i])

    return {"customer_status": cust_status[1], "cust_sts_hist": hist_lst}

from random import randint
from core.utils.days_between import days_between
from core.utils.con_details import con_details
from datetime import date
from core.data.data import periods
import inspect
from core.exceptions.invalid_input_exception import InvalidInput


def generate_contracts(value: int, con_type: int, sts_hist: dict):
    """
    creates customer contracts based on their
    status history
    -----------------------------------------
    args: "value" represent the number of contracts to be created

    "con_type" represent contract type

    "sts_hist" represent status history for a client
    -----------------------------------------
    return: a list containing the contract history for the client
    """

    if not isinstance(value, int) or value == 0:
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': value")

    if not isinstance(con_type, int) or con_type == 0:
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': con_type")

    if not isinstance(sts_hist, dict):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': sts_hist")

    contracts = []
    years_periods = []
    weights = [1.3, 1.2, 1.1]
    lst_len = len(sts_hist["cust_sts_hist"])

    for y in range(lst_len):
        if sts_hist["cust_sts_hist"][y]["customer_status"] == "Active":
            if y + 1 < lst_len:
                period = (
                    int(
                        days_between(
                            d1=sts_hist["cust_sts_hist"][y + 1]["change_date"],
                            d2=sts_hist["cust_sts_hist"][y]["change_date"],
                        )
                    )
                ) // 365

                if period >= 1:
                    years_periods.append(period)
            else:
                period = (
                    int(
                        days_between(
                            d1=date.today(),
                            d2=sts_hist["cust_sts_hist"][y]["change_date"],
                        )
                    )
                ) // 365
                if period >= 1:
                    years_periods.append(period)

    for i in years_periods:
        # period of 12 months
        if i == 1:
            contracts.append(con_details(12, 1.3))
        # period of 24 months
        elif i == 2:
            if randint(0, 9) < 4:
                for _ in range(i):
                    contracts.append(con_details(periods[1], weights[0]))
            else:
                contracts.append(con_details(periods[2], weights[1]))
        elif i == 0:
            if len(contracts) == 0:
                contracts.append(
                    {
                        "contract_title": "pgo",
                        "num_of_sims": 1,
                        "num_of_devices": 0,
                        "con_details": 0,
                        "devices": 0,
                        "price": 0,
                        "available_data": {
                            "calls_times": 0,
                            "cellular_data": 0.0,
                            "roam_data": 0.0,
                            "roam_call_time": 0,
                        },
                    }
                )
        # period is more than 24 months
        else:
            while i != 0:
                rand_num = randint(0, 9)
                if i >= 3:
                    if rand_num == 0:
                        contracts.append(con_details(periods[1], weights[0]))
                        i -= 1
                    elif rand_num < 3:
                        contracts.append(con_details(periods[2], weights[1]))
                        i -= 2
                    else:
                        contracts.append(con_details(periods[3], weights[2]))
                        i -= 3
                elif i == 2:
                    contracts.append(con_details(periods[2], weights[1]))
                    i -= 2
                else:
                    contracts.append(con_details(periods[1], weights[0]))
                    i -= 1
    if len(contracts) == 0:
        contracts.append(
            {
                "contract_title": "pgo",
                "num_of_sims": 1,
                "num_of_devices": 0,
                "con_details": 0,
                "devices": 0,
                "price": 0,
                "available_data": {
                    "calls_times": 0,
                    "cellular_data": 0.0,
                    "roam_data": 0.0,
                    "roam_call_time": 0,
                },
            }
        )

    return contracts

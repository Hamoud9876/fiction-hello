from random import randint
from core.utils.get_devices import get_devices
import inspect
from core.exceptions.invalid_input_exception import InvalidInput
from datetime import date, datetime


def con_details(period: int, weight: float, start_date: date):
    """
    creates a period contract data
    -----------------------------------------
    args: "period" represent the length of the contract
    in months

    "weight" representing the the profit on that period
    -----------------------------------------
    return: a dict containing the contract details for that period
    """
    if not isinstance(period, int) or period not in [12, 24, 36]:
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': period")

    if not isinstance(weight, float):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': weight")

    if not isinstance(start_date, (date, datetime)):
        func_name = inspect.currentframe().f_code.co_name
        raise InvalidInput(f"Invalid input in '{func_name}': date")

    num_of_devices = randint(1, 2)
    devices_lst = get_devices(num_of_devices)
    total_devices_price = 0

    for i in devices_lst:
        total_devices_price += i["price"]

    return {
        "contract_title": "contract title",
        "num_of_sims": randint(1, 2),
        "num_of_devices": num_of_devices,
        "con_period": period,
        "devices": devices_lst,
        "price": round((total_devices_price + (10 * period)) * weight, 2),
        "available_data": {
            "calls_times": 150,
            "cellular_data": 150.0,
            "roam_data": 50.0,
            "roam_call_time": 50,
        },
        "start_date": start_date,
    }

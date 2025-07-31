from datetime import date,datetime
from core.exceptions.invalid_input_exception import InvalidInput
from random import uniform, randint
from dateutil.relativedelta import relativedelta
import inspect

def customer_usage(period: int, start_date: date):
    """
    creates customer usage record pased on
    the contract period and start date
    -----------------------------------------
    args: "period" how many months the contracts last for

    "start_date" the month of which the contracts starts

    -----------------------------------------
    return: a list containing dictionries
    representing the customer usage for each month
    """
    func_name = inspect.currentframe().f_code.co_name
    if not isinstance(period, int) or period not in [12,24,36]:
        raise InvalidInput(f"Invalid input in '{func_name}': period")
    
    if not isinstance(start_date, (date,datetime)):
        raise InvalidInput(f"Invalid input in '{func_name}': start_date")
    usage_lst = []
    for i in range(period):
        usage_lst.append({
            "used_cellular_data": (round(uniform(30, 150.00),2) 
                                    if randint(0,20) != 0 
                                    else round(uniform(145.00, 200.00),2)),
            "used_call_time": (randint(30, 150) if randint(0,20) != 0
                               else randint(140, 180)),
            "used_roam_data": (round(uniform(0.00, 50.00),2) 
                               if randint(0,20) != 0
                               else 0.00),
            "used_roam_call_time": (randint(0, 50)
                                    if randint(0,20) != 0
                                    else 0),
            "start_date": (usage_lst[-1]["start_date"]
                           if len(usage_lst) >0
                           else start_date),
            "end_date": start_date +relativedelta(months=i)
        })
    return usage_lst
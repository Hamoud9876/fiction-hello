from core.exceptions.invalid_input_exception import InvalidInput
from core.data.data import charge_rate, billing_status
from datetime import date
from dateutil.relativedelta import relativedelta
from random import randint
import inspect

def generate_bellings(usage_lst: list):

    func_name = inspect.currentframe().f_code.co_name

    if not isinstance(usage_lst, list):
        raise InvalidInput(f"Invalid input in '{func_name}': period")
    
    
    usage_data_limit = 150000
    usage_call_limit = 150
    usage_roam_call_limit = 50
    usage_roam_data_limit = 50000
    billing_lst = []
    my_bill_status = 0
    
    for i in usage_lst:
        if i["start_date"] < date.today():
            total_amount = 0

            #convert from GB to MB as data charge rate is per MB
            data_usage = i["used_cellular_data"] * 1000
            if data_usage > usage_data_limit:
                extra_data_usage = data_usage - usage_data_limit
                total_amount += extra_data_usage * charge_rate["data_rate"]

            
            if i["used_call_time"] > usage_call_limit:
                call_usage = i["used_call_time"] - usage_call_limit
                total_amount += call_usage * charge_rate["call_rate"]

            #convert from GB to MB as data charge rate is per MB
            roam_data = i["used_roam_data"] * 1000
            if roam_data > usage_roam_data_limit:
                extra_roam_data_usage = roam_data - usage_roam_data_limit
                total_amount += extra_roam_data_usage * charge_rate["roam_data_rate"]
            
            if i["used_roam_call_time"] > usage_roam_call_limit:
                roam_call = i["used_roam_call_time"] - usage_roam_call_limit
                total_amount += roam_call * charge_rate["roam_call_rate"]

            #2.5% chance to be upaied 
            if my_bill_status == 1:
                current_bill_status = 1
            else:
                current_bill_status = 1 if randint(0,39) == 0 else 0

            billing_lst.append({
            "amount": total_amount,
            "status": (billing_status[0]
                       if current_bill_status == 0
                       else billing_status[1]),
            "issue_date": i["end_date"] - relativedelta(days= 7),
            "complete_date": (i["end_date"] + relativedelta(days=randint(0,5))
                               if current_bill_status == 0
                               else None),
            "due_date": i["end_date"]
            })
        else: 
            #only triggered when the hit a future date
            break

        my_bill_status = current_bill_status
        
    return billing_lst


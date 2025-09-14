from random import randint
from core.utils.days_between import days_between
from core.utils.con_details import con_details
from datetime import date
from core.data.data import periods
import inspect
from core.exceptions.invalid_input_exception import InvalidInput
from dateutil.relativedelta import relativedelta


def generate_contracts(value: int, con_type: int, sts_hist: dict):
    """
    creates customer contracts based on their
    status history
    -----------------------------------------
    args: "value" represent the number of contracts to be created

    "con_type" represent contract type_id

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
    years_periods = {"periods": []}
    weights = [1.3, 1.2, 1.1]
    lst_len = len(sts_hist["cust_sts_hist"])

    for y in range(lst_len):
        if sts_hist["cust_sts_hist"][y]["customer_status"] == "Active":
            # checking if there is a status change after this one
            # and returning the period difference between them
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
                    years_periods["periods"].append(
                        {
                            "period": period,
                            "start_date": sts_hist["cust_sts_hist"][y]["change_date"],
                        }
                    )

            # last change in history
            # returns the diff between the date of the change until today
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
                    years_periods["periods"].append(
                        {
                            "period": period,
                            "start_date": sts_hist["cust_sts_hist"][y]["change_date"],
                        }
                    )

    for i in years_periods["periods"]:
        # period of 12 months
        if i["period"] == 1:
            contracts.append(con_details(12, 1.3, i["start_date"]))

        # period of 24 months
        elif i["period"] == 2:
            if randint(0, 9) < 4:
                for x in range(len(i)):
                    effective_date = i["start_date"] + relativedelta(months=x * 12)
                    contracts.append(
                        con_details(periods[1], weights[0], effective_date)
                    )
            else:
                contracts.append(con_details(periods[2], weights[1], i["start_date"]))

        # period is more than 24 months
        else:
            effective_date = i["start_date"]
            # splitting the period into multiple contracts
            while i["period"] != 0:
                rand_num = randint(0, 9)
                if i["period"] >= 3:

                    # %10 chance to create a 1 year contract when the total years is 3 or more
                    if rand_num == 0:
                        effective_date = effective_date + relativedelta(months=12)
                        contracts.append(
                            con_details(periods[1], weights[0], effective_date)
                        )
                        i["period"] -= 1

                    # %20 chance to create a 2 year contract when the total years is 3 or more
                    elif rand_num < 3:
                        effective_date = effective_date + relativedelta(months=24)
                        contracts.append(
                            con_details(periods[2], weights[1], effective_date)
                        )
                        i["period"] -= 2

                    # %70 chance to create a 3 year contract when the total years is 3 or more
                    else:
                        effective_date = effective_date + relativedelta(months=36)
                        contracts.append(
                            con_details(periods[3], weights[2], effective_date)
                        )
                        i["period"] -= 3

                elif i["period"] == 2:
                    # %30 chance to create a 1 year contract when the total years is 2 or more
                    if rand_num < 3:
                        effective_date = effective_date + relativedelta(months=12)
                        contracts.append(
                            con_details(periods[1], weights[0], effective_date)
                        )
                        i["period"] -= 1

                    else:
                        # %70 chance to create a 2 year contract when the total years is 2 or more
                        effective_date = effective_date + relativedelta(months=24)
                        contracts.append(
                            con_details(periods[2], weights[1], effective_date)
                        )
                        i["period"] -= 2

                else:
                    # creating a one year contract if the total years is 1
                    effective_date = effective_date + relativedelta(months=12)
                    contracts.append(
                        con_details(periods[1], weights[0], effective_date)
                    )
                    i["period"] -= 1

    # if the customer total join period was less than a year
    if len(contracts) == 0:
        contracts.append(
            {
                "contract_title": "pgo",
                "num_of_sims": 1,
                "num_of_devices": 0,
                "con_period": 0,
                "devices": 0,
                "price": 0,
                "available_data": {
                    "calls_times": 0,
                    "cellular_data": 0.0,
                    "roam_data": 0.0,
                    "roam_call_time": 0,
                },
                "start_date": sts_hist["cust_sts_hist"][0]["change_date"],
            }
        )

    return contracts

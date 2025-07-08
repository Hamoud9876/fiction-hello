from random import randint
from core.utils.get_devices import get_devices
from core.utils.random_string import random_string



def periods_generator(period: int, weight: float):
    if not isinstance(period, int) or period not in [12,24,36]:
        return "Invalid input for period"
    if not isinstance(weight,float):
        return "Invalid input for weight"
    
    num_of_devices = randint(1,2)
    devices_lst = get_devices(num_of_devices)
    total_devices_price = 0

    for i in devices_lst:
        total_devices_price += i["price"]

    return {
    "contract_title" : random_string(randint(5,20)),
    "num_of_sims" : randint(1,2),
    "num_of_devices" : num_of_devices,
    "con_period" : period,
    "devices": devices_lst,
    "price": round((total_devices_price + (10* period) ) * weight,2),
        }


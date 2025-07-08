from core.data.data import laptops_details
from core.data.data import watchs_details
from core.data.data import tablets_details
from core.data.data import router_details
from core.data.data import phones_details
from random import randint


def get_devices(num_devices: int):
    if not isinstance(num_devices, int) or num_devices == 0:
        return "Invalid value for number of devices"
    
    picker = randint(0,19)
    devices_lst = []
    for _ in range(num_devices):
        #40% to be a phone
        if picker >= 8:
            devices_lst.append(phones_details[randint(0,5)])
        #25% chance for a home router
        elif picker <= 13:
            devices_lst.append(router_details[randint(0,2)])
        #25% chance for a tablet
        elif picker <= 17:
            devices_lst.append(tablets_details[randint(0,2)])
        #5% chance for a labtop 
        elif picker <= 18:
            devices_lst.append(laptops_details[randint(0,2)])
        #5% chance for a smartwatch
        else:
            devices_lst.append(watchs_details[randint(0,2)])
    
    return devices_lst

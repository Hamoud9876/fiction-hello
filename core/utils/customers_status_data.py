from core.data.data import customers_status
from random import randint
from core.utils.cust_hist_active import cust_hist_active
from core.utils.cust_hist_inactive import cust_hist_inactive
from datetime import date, datetime
from faker import Faker

def customers_status_data(join_date: date, cust_id:int):
    if (not isinstance(join_date, date) 
        or not isinstance(cust_id,int) ):
        return "Not a valid input"
    rand_num = randint(0,9)
    
    #customer active since joining
    if rand_num >2:
        cust_hist_active(customers_status, join_date,cust_id)

    #customer not active anynore
    elif rand_num ==2:
        cust_hist_inactive(customers_status, join_date,cust_id)
        
    #complecated history of multiple changes
    elif rand_num > 7:
        pass
    #complecated history of departure or blocked
    else:
        pass


    rand_num = randint(0,3)
    customer_status = customers_status[rand_num]
    return {"customer_status": customer_status,
            }
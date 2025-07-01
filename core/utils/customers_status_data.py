from core.data.data import customers_status
from random import randint
from core.utils.cust_hist_active import cust_hist_active
from core.utils.cust_hist_inactive import cust_hist_inactive
from core.utils.cust_hist_long_changes import cust_hist_long_changes
from datetime import date, datetime
from faker import Faker

def customers_status_data(join_date: date, cust_id:int):
    if (not isinstance(join_date, date) 
        or not isinstance(cust_id,int) ):
        return "Not a valid input"
    rand_num = randint(0,9)
    
    #customer active since joining
    if rand_num >3:
        return cust_hist_active(customers_status, join_date,cust_id)

    #customer not active anynore
    elif rand_num ==3:
        return cust_hist_inactive(customers_status, join_date,cust_id)
        
    #complecated history of multiple changes
    else:
        return cust_hist_long_changes(customers_status, join_date,cust_id)
    

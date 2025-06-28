


def generate_customers_data(cust_dict: dict):
    """
    creates a random customers details
    -----------------------------------------
    args: "cust_dict" represent available customer
    -----------------------------------------
    return: a dict containing a list of contracts
    """

    if (not isinstance(cust_dict,dict) 
        or "customers" not in cust_dict
        or not isinstance(cust_dict["customers"],list)
        or len(cust_dict["customers"]) == 0 ):
        return "Not a valid dict"
    
    
    
    
    return {"contracts": []}

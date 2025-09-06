import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def transform_customers_usage(df_cust_usage):
    """
    transform the provided tables/df into facr_customer_usage
    table structure.
    -----------------------------------------
    args: 
    df_cust_usage: df contaning the customers usage data.
    -----------------------------------------
    return: datafram contaning exact structure of
    facr_customer_usage table.
    """

    logger.info("started transforming customers_usage")

    
    

    try:

        df_copy_cust_usage = df_cust_usage.copy()

        if df_copy_cust_usage.empty:
            return df_copy_cust_usage
        
        #making sure the dates types are correct
        df_copy_cust_usage["start_date"] = df_copy_cust_usage["start_date"].dt.date
        df_copy_cust_usage["end_date"] = df_copy_cust_usage["end_date"].dt.date


    except Exception as e:
        logger.error(f"failed to transform customers_usage: {e}")

    logger.info("finished transforming customers_usage")

    return df_copy_cust_usage


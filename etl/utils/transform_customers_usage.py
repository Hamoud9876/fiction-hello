


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

    if df_cust_usage.empty:
        return df_cust_usage

    #making sure the dates types are correct
    df_cust_usage["start_date"] = df_cust_usage["start_date"].dt.date
    df_cust_usage["end_date"] = df_cust_usage["end_date"].dt.date


    return df_cust_usage


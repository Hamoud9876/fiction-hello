import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_customers_demo(df_location,df_cust_address):
    """
    transform the provided tables/df into 
    tact_customers_demographic table structure
    -----------------------------------------
    args: 
    df_location: df contaning the location data.

    df_cust_address: df contaning the 
    location_id and customers_id data.
    -----------------------------------------
    return: datafram contaning exact structure of
    tact_customers_demographic table
    """
    
    logger.info("started transforming customers_demo")

    df_cust_demo = df_location.copy()
    df_copy_cust_address = df_cust_address.copy

    #merging the dfs together
    df_cust_demo = df_cust_demo.merge(df_copy_cust_address, on="location_id", how="left")


    #converting the date time into date to be used in the fact table
    df_cust_demo["last_updated"] = df_cust_demo["last_updated"].dt.date

    #removing unwanted columns
    df_cust_demo.drop(["city", "county","post_code",
                   "address_type", "full_address"],axis=1,  inplace=True)
    
    logger.info("finished transforming customers_demo")

    return df_cust_demo
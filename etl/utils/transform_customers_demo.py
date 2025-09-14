import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_customers_demo(df_cust_address):
    """
    transform the provided tables/df into
    tact_customers_demographic table structure
    -----------------------------------------
    args:

    df_cust_address: df contaning the
    location_id and customers_id data.
    -----------------------------------------
    return: datafram contaning exact structure of
    tact_customers_demographic table
    """

    logger.info("started transforming customers_demo")

    try:
        df_copy_cust_address = df_cust_address.copy()

        # removing unwanted columns
        df_copy_cust_address.drop(["customers_address_id"], axis=1, inplace=True)

    except Exception as e:
        logger.error(f"failed to transform customers_demo: {type(e).__name__}: {e}")
    logger.info("finished transforming customers_demo")

    return df_copy_cust_address

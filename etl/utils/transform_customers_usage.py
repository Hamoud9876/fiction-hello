import logging
import pandas as pd


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

        # making sure the dates types are correct
        df_copy_cust_usage["start_date"] = pd.to_datetime(
            df_copy_cust_usage["start_date"]
        ).dt.date
        df_copy_cust_usage["end_date"] = pd.to_datetime(
            df_copy_cust_usage["end_date"]
        ).dt.date

        # keeping only wanted columns
        df_copy_cust_usage = df_copy_cust_usage[
            [
                "customer_id",
                "used_cellular_data",
                "used_call_time",
                "used_roam_call_time",
                "used_roam_data",
                "start_date",
                "end_date",
            ]
        ]

    except Exception as e:
        logger.error(f"failed to transform customers_usage: {type(e).__name__}: {e}")

    logger.info("finished transforming customers_usage")

    return df_copy_cust_usage

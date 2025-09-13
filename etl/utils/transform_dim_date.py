import pandas as pd
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_dim_date(**kwargs):
    """
    transform the provided dictionary of dfs
    into dim_date table structure
    -----------------------------------------
    args: 
    kwargs: takes any number of key value pairs as input
    (expected it to be df_name and the df conten)
    -----------------------------------------
    return: datafram contaning exact structure of dim_date table
    """

    all_dates = []

    logger.info("started transforming dim_date")

    #creating an empty dim_date to make sure there is always some columns
    #in my return df
    dim_date = pd.DataFrame(columns=[
    "date_id", "day", "month", "year", "day_of_week", "day_name", "quarter"
])

    try:
        #added only data from columns that are subtype of datetime
        #to the date list, also making sure any date field gets casted
        #to the correct data type
        for df_name, df in kwargs.items():
            if df.empty:
                continue
            
            if df_name == "customers":
                df["birthdate"] = pd.to_datetime(df["birthdate"]).dt.date
                df["join_date"] = pd.to_datetime(df["join_date"]).dt.date

            if df_name == "billing":
                df["issue_date"] = pd.to_datetime(df["issue_date"]).dt.date
                df["completed_date"] = pd.to_datetime(df["completed_date"]).dt.date
                df["due_date"] = pd.to_datetime(df["due_date"]).dt.date

            if df_name in ["customer_status_history","billing_status_history"]:
                df["change_date"] = pd.to_datetime[df["change_date"]].dt.date

            if df_name in ["customers_usage","charge_rates",
            "address", "personal_data"]:
                df["start_date"] = pd.to_datetime(df["start_date"])
                df["end_date"] = pd.to_datetime(df["end_date"])

            for col in df.columns:
                if np.issubdtype(df[col].dtype, np.datetime64):
                    all_dates.append(df[col].dropna())


        #added all the collected dates in the list to a dataframe
        if all_dates:
            all_dates = pd.concat(all_dates).drop_duplicates().reset_index(drop=True)
            dim_date = pd.DataFrame({"date_id": all_dates,
                                    "day": all_dates.dt.day,
                                    "month": all_dates.dt.month,
                                    "year": all_dates.dt.year,
                                    "day_of_week": all_dates.dt.dayofweek,
                                    "day_name": all_dates.dt.day_name(),
                                    "quarter": all_dates.dt.quarter})
        else:
            logger.info("no dates columns found")
            return pd.DataFrame(columns=[
                "date_id", 
                "day", 
                "month", 
                "year", 
                "day_of_week", 
                "day_name", 
                "quarter"
            ])

    except Exception as e:
        logger.error(f"failed to transform dim_date: {type(e).__name__}: {e}")


    logger.info("finished transforming dim_date")
    
    return dim_date

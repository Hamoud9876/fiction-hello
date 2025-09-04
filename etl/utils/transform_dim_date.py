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

    try:
        for df_name, df in kwargs.items():
            for col in df.columns:
                if df[col].dtype == 'object':
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except Exception:
                        continue
            
                if np.issubdtype(df[col].dtype, np.datetime64):
                    all_dates.append(df[col].dropna())

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
        logger.error(f"failed to transform dim_date: {e}")


    logger.info("finished transforming dim_date")
    
    return dim_date

import pandas as pd
import numpy as np


def transform_dim_date(**kwargs):

    all_dates = []

    for df_name, df in kwargs.items():
        for col in df.columns:
            if np.issubdtype(df[col].dtype, np.datetime64):
                all_dates.append(df[col].dropna())

    all_dates = pd.concat(all_dates).drop_duplicates().reset_index(drop=True)
    dim_date = pd.DataFrame({"date_id": all_dates,
                            "day": all_dates.dt.day,
                            "month": all_dates.dt.month,
                            "year": all_dates.dt.year,
                            "day_of_week": all_dates.dt.dayofweek,
                            "day_name": all_dates.dt.day_name(),
                            "quarter": all_dates.dt.quarter})
    
    return dim_date

import pandas as pd


def transform_personal_data(df_personal_data):
    """
    transform the provided tables/df into dim_personal_data table structure

    Args:
        df_personal_data: df contaning the address data.
        df_address_type: df contaning the addres type data.

    Return:
        datafram contaning exact structure of dim_personal_data table
    """

    copy_df = df_personal_data.copy()

    # making sure dates are in the right format
    copy_df["start_date"] = pd.to_datetime(copy_df["start_date"]).dt.date
    copy_df["end_date"] = pd.to_datetime(copy_df["end_date"]).dt.date

    # making sure to only keep wanted columns
    copy_df = copy_df[
        [
            "personal_data_id",
            "avail_calls_time",
            "avail_cellular_data",
            "avail_roam_data",
            "avail_roam_calls_time",
            "start_date",
            "end_date",
        ]
    ]

    return copy_df

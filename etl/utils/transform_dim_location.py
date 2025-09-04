import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_dim_location(df_address, df_address_type):
    """
    transform the provided tables/df into dim_location table structure
    -----------------------------------------
    args: 
    df_address: df contaning the address data.

    df_address_type: df contaning the addres type data.
    -----------------------------------------
    return: datafram contaning exact structure of dim_location table
    """

    logger.info("started transforming dim_location")


    address = []

    try:
        df_address["second_line"] = df_address["second_line"].fillna("")

        for inx, row in df_address.iterrows():
            parts = [row["first_line"]]

            if row["second_line"]:
                parts.append(row["second_line"])

            address.append(", ".join(parts))


        #assigning the new address to a new column
        df_address["full_address"] = address
        

        #merging on address type id to get the text for each address
        df_address = df_address.merge(df_address_type, on="address_type_id", how="left")


        #dropping unwanted columns
        df_address = df_address.drop("address_type_id", axis=1)
        df_address = df_address.drop("first_line", axis=1)
        df_address = df_address.drop("second_line", axis=1)

    except Exception as e:
        logger.error("faild to transform dim_location")

    logger.info("finished transforming dim_location")


    return df_address
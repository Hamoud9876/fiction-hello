import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_dim_location(df_address, df_address_type):
    """
    transform the provided tables/df into dim_location table structure

    Args:
        df_address: df contaning the address data.
        df_address_type: df contaning the addres type data.

    Return:
        datafram contaning exact structure of dim_location table
    """

    logger.info("started transforming dim_location")

    address = []

    try:
        # copying the dfs to preserve the original from any changes
        df_copy_address = df_address.copy()
        df_copy_address_type = df_address_type.copy()

        # making sure any empty address are filled with empty string
        df_copy_address["second_line"] = df_copy_address["second_line"].fillna("")

        # joining address parts to make full address
        # without added ampty string
        for inx, row in df_copy_address.iterrows():
            parts = [row["first_line"]]

            if row["second_line"]:
                parts.append(row["second_line"])

            address.append(", ".join(parts))

        # assigning the new address to a new column
        df_copy_address["full_address"] = address

        # merging on address type id to get the text for each address
        df_copy_address = df_copy_address.merge(
            df_copy_address_type, on="address_type_id", how="left"
        )

        df_copy_address.rename(columns={"address_id": "location_id"}, inplace=True)

        # keeping only wanted columns
        df_copy_address = df_copy_address[
            [
                "location_id",
                "full_address",
                "city",
                "county",
                "post_code",
                "address_type",
            ]
        ]

    except Exception as e:
        logger.error(f"faild to transform dim_location: {type(e).__name__}: {e}")

    logger.info("finished transforming dim_location")

    return df_copy_address

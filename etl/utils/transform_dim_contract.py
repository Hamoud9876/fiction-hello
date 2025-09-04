import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_dim_contract(df_contracts, df_contracts_details, df_periods, df_contract_type):
    """
    transform the provided tables/df into dim_contract table structure
    -----------------------------------------
    args: 
    df_contracts: df contaning the contracts data.

    df_contracts_details: df contaning the contracts details data.
   
    df_periods: df contaning the preiods data.

    df_contract_type: df contaning the contract types data.
    -----------------------------------------
    return: datafram contaning exact structure of dim_contract table
    """

    logger.info("started to transform dim_contracts")

    df =  df_contracts_details.copy()
    try:
        #mergning all the dfs
        df = df.merge(df_periods, on="contract_period_id", how="left")
        df = df.merge(df_contracts, on="contract_details_id", how="left")
        df = df.merge(df_contract_type, on="contract_type_id", how="left")


        #using initial and discount to get the effective price
        df["effective_price"] = np.where(
        df["discount_percent"] > 0,
        df["initial_price"] * (1 - df["discount_percent"]/100),
        df["initial_price"]
        ).round(2)


        #renaming the column that were merged to match the distenation table
        df.rename(columns={"period": "contract_period"}, inplace=True)

        #droppping unwanted columns
        df = df.drop(["contract_details_id", "contract_type_id", "contract_period_id"], axis=1)

    except Exception as e:
        logger.error(f"falied to transform dim_contract: {e}")

    logger.info("finished transforming dim_contract")
    return df
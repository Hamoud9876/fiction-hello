import pandas as pd
import logging



logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def transform_customers_contracts(df_cust_con, df_con, df_con_details,df_periods):
    """
    transform the provided tables/df into fact_customers_contracts
    table structure
    -----------------------------------------
    args: 
    df_cust_con: df contaning the customer contract data.

    df_con: df contaning the contracts data.
   
    df_con_details: df contaning the contracts details data.

    df_periods: df contaning the period data.
    -----------------------------------------
    return: datafram contaning the structure of 
    fact_customers_contracts table
    """

    logger.info(f"transforming customers_contracts started")

    
    try:
        #copying the dfs to preserve the original from any changes
        df_copy_cust_con = df_cust_con.copy()
        df_copy_con = df_con.copy()
        df_copy_con_details = df_con_details.copy()
        df_copy_periods = df_periods.copy()


        #if the cust contract is empty then nothing diretly
        #changed in the ownership of the contract
        if df_copy_cust_con.empty:
            logger.info(f"df_cust_con was empty")
            return df_copy_cust_con
        

        #if mothing changed in the contract of its details then 
        #only the owner ship of the contract is different
        if df_copy_con.empty or df_copy_con_details.empty:
            logger.info(f"df_con or df_con_details was empty")
            return df_copy_cust_con
        
        
        #droping unwated dates to avoid suffixes clashing when merged
        df_copy_con.drop(["last_updated","created_at"],axis=1,  inplace=True)
        df_copy_con_details.drop(["last_updated","created_at"],axis=1,  inplace=True)
        df_copy_periods.drop(["last_updated","created_at"],axis=1,  inplace=True)


        #merging period with contract details
        df_copy_con_details = df_copy_con_details.merge(df_copy_periods,on="contract_period_id",
                                            how="left" )

        #re-shaping the contract details df to only contains wanted series
        df_copy_con_details = df_copy_con_details[["contract_details_id", "period"]]


        #mergiing contracts details with contracts
        df_copy_con = df_copy_con.merge(df_copy_con_details,on="contract_details_id",how="left")


        #re-shaping the contracts df to only contains wanted series
        df_copy_con = df_copy_con[["contract_id","period"]]


        #mergiing customers contracts with contracts
        df_copy_cust_con = df_copy_cust_con.merge(df_copy_con, on="contract_id",how="left")


        #making sure the date are in the correct format
        df_copy_cust_con["created_at"] = df_copy_cust_con["created_at"].dt.date
        df_copy_cust_con["last_updated"] = df_copy_cust_con["last_updated"].dt.date

        #setting start date and end date of the contract
        df_copy_cust_con["start_date"] = df_copy_cust_con["created_at"]
        df_copy_cust_con["end_date"] =  df_copy_cust_con.apply(
            lambda row: row["start_date"] + pd.DateOffset(months=row["period"]),
            axis=1
        )


        #checking if the contract is still active
        df_copy_cust_con["is_active"] = df_copy_cust_con["end_date"] > pd.Timestamp.now()



        #keeping only the wanted columns
        df_copy_cust_con = df_copy_cust_con[["customer_id","contract_id","start_date",
                                             "end_date", "is_active"]]
    except Exception as e:
        logger.error(f"failed to transform customers_contracts: {type(e).__name__}: {e}")

    logger.info("finished transforming customers contracts")

    
    return df_copy_cust_con
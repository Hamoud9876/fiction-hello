import pandas as pd
import logging


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def transform_dim_customers(df_customer, df_gender, df_pronounce, df_cust_sts):
    """
    transform the provided tables/df into dim_customers table structure
    -----------------------------------------
    args: 
    df_customer: df contaning the customer data.

    df_gender: df contaning the gender data.
   
    df_pronounce: df contaning the pronounce data.

    df_cust_sts: df contaning the customer status data.
    -----------------------------------------
    return: datafram contaning exact structure of dim_custoemrs table
    """

    logger.info("started transforming dim_customers")


    try:
        #copying the dfs to preserve the original from any changes
        df_copy_gender = df_gender.copy()
        df_copy_pronounce = df_pronounce.copy()
        df_copy_cust_sts = df_cust_sts.copy()
        df_copy_customer = df_customer.copy()


        #making sure dates are correct
        df_copy_customer["birthdate"] = pd.to_datetime(df_copy_customer["birthdate"])
        df_copy_customer["birthdate"] = df_copy_customer["birthdate"].dt.date
        df_copy_customer["join_date"] = pd.to_datetime(df_copy_customer["join_date"])
        df_copy_customer["join_date"] = df_copy_customer["join_date"].dt.date


        #droping unwated dates to avoid suffixes clashing when merged
        df_copy_gender.drop(["last_updated","created_at"], axis=1, inplace=True)
        df_copy_pronounce.drop(["last_updated","created_at"],axis=1,  inplace=True)
        df_copy_cust_sts.drop(["last_updated","created_at"],axis=1,  inplace=True)
        

        #filling all the empty middle name series with empty string
        df_copy_customer["middle_name"] = df_copy_customer["middle_name"].fillna("")


        full_names = []
        ages = []
        age_group = []
        today = pd.Timestamp("today")


        for idx, row in df_copy_customer.iterrows():
            #merging name sigments into one full name
            parts = [row["first_name"]]
            if row["middle_name"]:  
                parts.append(row["middle_name"])
            parts.append(row["last_name"])
            full_names.append(" ".join(parts))


            #retrieving the age from the birthdate
            ages.append(today.year - row["birthdate"].year - 
                    ((today.month, today.day) < (row["birthdate"].month, row["birthdate"].day)))


            #deciding the age group based on age
            if ages[-1] >=18 and ages[-1] <=28:
                age_group.append("18 - 25")
            elif ages[-1] >=26 and ages[-1] <=30:
                age_group.append("26 - 30")
            elif ages[-1] >=31 and ages[-1] <=39:
                age_group.append("31 - 39")
            else:
                age_group.append("40+")
        

        #mergning the others df to create a new df that matches the destenation table
        df_copy_customer = df_copy_customer.merge(df_copy_gender, on="gender_id", how="left")
        df_copy_customer = df_copy_customer.merge(df_copy_pronounce, on="pronounce_id", how="left")
        df_copy_customer = df_copy_customer.merge(df_copy_cust_sts, on="customer_status_id", how="left")


        #making sure that it is date type as expected
        df_copy_customer["join_date"] = pd.to_datetime(df_copy_customer["join_date"]).dt.date
        

        #renaming the column that were merged to match the distenation table
        df_copy_customer.rename(columns={"gender_title": "gender",
                                    "pronounce_title": "pronounce",
                                    "status": "customer_status"},
                                    inplace=True)



        #adding the new column to the df
        df_copy_customer["full_name"] = full_names
        df_copy_customer["age"] = ages
        df_copy_customer["age_group"] = age_group


        #keeping only wanted columns
        df_copy_customer = df_copy_customer[["join_date","full_name","gender",
                                            "pronounce","customer_status","age",
                                            "age_group","customer_id"]]

    except Exception as e:
        logger.error(f"failed to transform dim_customers: {type(e).__name__}: {e}")

    logger.info("finished transforming dim_customers")

    return df_copy_customer
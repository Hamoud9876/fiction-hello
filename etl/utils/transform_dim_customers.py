import pandas as pd
import logging


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def transform_dim_customers(df_customer, df_gender, df_pronounce, df_cust_sts):
    """
    transform the provided tables into dim_customers table structure
    -----------------------------------------
    args: 
    df_customer: df contaning the customer data.

    df_gender: df contaning the gender data.
   
    df_pronounce: df contaning the pronounce data.

    df_cust_sts: df contaning the customer status data.
    -----------------------------------------
    return: datafram contaning exact structure of dim_custoemrs table
    """
    #filling all the empty middle name series with empty string
    df_customer["middle_name"] = df_customer["middle_name"].fillna("")


    full_names = []
    ages = []
    age_group = []
    today = pd.Timestamp("today")


    for idx, row in df_customer.iterrows():
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
    df_customer = df_customer.merge(df_gender, on="gender_id", how="left")
    df_customer = df_customer.merge(df_pronounce, on="pronounce_id", how="left")
    df_customer = df_customer.merge(df_cust_sts, on="customer_status_id", how="left")


    #making sure that it is date type as expected
    df_customer["join_date"] = pd.to_datetime(df_customer["join_date"]).dt.date
    

    #renaming the column that were merged to match the distenation table
    df_customer.rename(columns={"gender_title": "gender",
                                "pronounce_title": "pronounce",
                                "status": "customer_status"},
                                inplace=True)



    #adding the new column to the df
    df_customer["full_name"] = full_names
    df_customer["age"] = ages
    df_customer["age_group"] = age_group


    #dropping unwated columns to match the distenation table
    df_customer = df_customer.drop("first_name", axis=1)
    df_customer = df_customer.drop("middle_name", axis=1)
    df_customer = df_customer.drop("last_name", axis=1)
    df_customer = df_customer.drop("birthdate", axis=1)
    df_customer = df_customer.drop("last_updated", axis=1)
    df_customer = df_customer.drop("gender_id", axis=1)
    df_customer = df_customer.drop("pronounce_id", axis=1)
    df_customer = df_customer.drop("customer_status_id", axis=1)


    return df_customer
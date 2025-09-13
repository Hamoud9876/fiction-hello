from datetime import date
import pandas as pd
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def transform_billing(df_billing, df_billing_status):
    """
    transform the provided tables/df into facr_billing
    table structure.
    -----------------------------------------
    args: 
    df_billing: df contaning the billing data.
    df_billing_status: df contaning the billing status data.
    -----------------------------------------
    return: datafram contaning exact structure of
    fact_billing table.
    """

    logger.info("started transforming billing")

    try:
        #copying the dfs to preserve the original from any changes
        df_copy_billing = df_billing.copy()
        df_copy_billing_status = df_billing_status.copy()

        #making sure dates are in the correct type
        df_copy_billing["issue_date"] = pd.to_datetime(df_copy_billing["issue_date"])
        df_copy_billing["completed_date"] = pd.to_datetime(df_copy_billing["completed_date"])
        df_copy_billing["due_date"] = pd.to_datetime(df_copy_billing["due_date"])


        #droping unwated columns to aviod clashing when merged
        df_copy_billing_status.drop(["last_updated","created_at"],axis=1,  inplace=True)


        #making sure dates are in the correct datatype
        df_copy_billing["completed_date"] = df_copy_billing["completed_date"].dt.date
        df_copy_billing["issue_date"] = df_copy_billing["issue_date"].dt.date
        df_copy_billing["due_date"] = df_copy_billing["due_date"].dt.date


        #filling empty completed date with a base date
        df_copy_billing["completed_date"] = df_copy_billing["completed_date"].fillna(
            date(year=1995,day=1,month=1))


        #getting the status descreption
        df_copy_billing = df_copy_billing.merge(df_copy_billing_status, on="bill_status_id", how="left")


        #getting the billed and paid amount
        df_copy_billing["amount_billed"] = df_copy_billing["amount"]
        df_copy_billing["amount_paid"] = df_copy_billing.apply(
            lambda row: row["amount"] 
            if row["status"] == "paid" else 0,
            axis=1)


        #setting the is_paid value
        df_copy_billing["is_paid"] = df_copy_billing.apply(
            lambda row: True 
            if row["status"]== "paid" else False,
            axis=1)


        #calculating overdue days
        df_copy_billing["days_overdue"] = df_copy_billing.apply(
            lambda row: 0 
            if row["due_date"] >= row["completed_date"] 
            else (row["completed_date"] -row["due_date"] ).days,
            axis=1 )

        #renaming columns
        df_copy_billing.rename(columns={"status": "bill_status",
                                        "completed_date":"complete_date"},
                                         inplace=True)

        #dropping unwated columns
        df_copy_billing = df_copy_billing[["customer_id", "contract_id","amount_billed",
                                           "amount_paid", "is_paid","days_overdue",
                                            "bill_status", "issue_date", "complete_date",
                                            "due_date","created_at", "last_updated"]]

    except Exception as e:
        logger.error(f"failed to transform billing: {type(e).__name__}: {e}")


    logger.info("finished transforming billing")


    return df_copy_billing

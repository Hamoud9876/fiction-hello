from datetime import date

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

    #making sure dates are in the correct datatype
    df_billing["completed_date"] = df_billing["completed_date"].dt.date
    df_billing["issue_date"] = df_billing["issue_date"].dt.date
    df_billing["due_date"] = df_billing["due_date"].dt.date

    #filling empty completed date with a base date
    df_billing["completed_date"] = df_billing["completed_date"].fillna(
        date(year=1995,day=1,month=1))

    #getting the status descreption
    df_billing = df_billing.merge(df_billing_status, on="bill_status_id", how="left")

    #getting the billed and paid amount
    df_billing["amount_billed"] = df_billing["amount"]
    df_billing["amount_paid"] = df_billing.apply(
        lambda row: row["amount"] 
        if row["status"] == "paid" else 0,
        axis=1)

    #setting the is_paid value
    df_billing["is_paid"] = df_billing.apply(
        lambda row: True 
        if row["status"]== "paid" else False,
        axis=1)

    #calculating overdue days
    df_billing["days_overdue"] = df_billing.apply(
        lambda row: 0 
        if row["due_date"] >= row["completed_date"] 
        else (row["completed_date"] -row["due_date"] ).days,
        axis=1 )


    #dropping unwated columns
    df_billing.drop(["bill_status_id","amount"],axis=1,inplace=True)

    #renaming columns
    df_billing.rename(columns={"status": "bill_status"}, inplace=True)


    return df_billing

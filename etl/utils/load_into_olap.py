from etl.database.db_connection_olap import db_connection, close_db
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def insert_df_into_db(df, table_name):
    """
    insert the provided df into the provided table
    
    Args: 
        df: dataframe that contains data to be insert
        table_name: table name

    
    Return:
        None
    """

    conflict_strategies = {
    "dim_date": "ON CONFLICT (date_id) DO NOTHING",
    "dim_customers": "ON CONFLICT (customer_id) DO UPDATE SET {updates}",
    "dim_contract": "ON CONFLICT (contract_id) DO UPDATE SET {updates}",
    "dim_location": "ON CONFLICT (contract_id) DO UPDATE SET {updates}",
    }
    try:
        conn = db_connection()

        for _, row in df.iterrows():
            cols = ",".join(row.index)
            placeholders = ",".join([f":{c}" for c in row.index])
            sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            if table_name in conflict_strategies:
                conflict = conflict_strategies[table_name]

            if "{updates}" in conflict:
                updates = ",".join([f"{c} = EXCLUDED.{c}" 
                                    for c in row.index 
                                    if c not in ("date_id", "customer_id", "contract_id","location_id")])
                conflict = conflict.format(updates=updates)

            sql = f"{sql} {conflict}"

            conn.run(sql, **row.to_dict())

            close_db(conn)
    except Exception as e:
        logger.info(f"failed to insert into table: {table_name}, {type(e).__name__}: {e}")

    
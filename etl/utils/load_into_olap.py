import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import logging
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def load_into_olap(table_df: pd.DataFrame, table: str):
    """
    Insert a DataFrame into a PostgreSQL table using pg8000,
    skipping rows that would violate unique/primary key constraints.

    Args:
        table_df (pd.DataFrame): DataFrame to insert
        table (str): Target table name

    Returns:
        str: Status message
    """
    try:
        # Create DB connection URL
        con_url = URL.create(
            drivername="postgresql+pg8000",
            host=os.getenv("DB_OLAP_HOST"),
            port=int(os.getenv("DB_OLAP_PORT")),
            database=os.getenv("DB_OLAP_DATABASE"),
            username=os.getenv("DB_OLAP_USERNAME"),
            password=os.getenv("DB_OLAP_PASSWORD"),
        )
        engine = create_engine(con_url, client_encoding="utf8")

        try:
            logger.info(f">>>> Attempting to write data to {table} <<<<")

            with engine.begin() as conn:
                # Fetch the primary key column(s) for the table
                pk_query = text(f"""
                    SELECT a.attname
                    FROM   pg_index i
                    JOIN   pg_attribute a 
                           ON a.attrelid = i.indrelid
                          AND a.attnum = ANY(i.indkey)
                    WHERE  i.indrelid = '{table}'::regclass
                    AND    i.indisprimary;
                """)
                pk_result = conn.execute(pk_query).fetchall()

                if pk_result:
                    pk_columns = [row[0] for row in pk_result]  # supports multi-column PKs
                    existing_df = pd.read_sql(
                        f"SELECT {', '.join(pk_columns)} FROM {table}", conn
                    )

                    before_count = len(table_df)

                    # Drop duplicates by checking PK values
                    if len(pk_columns) == 1:
                        pk_column = pk_columns[0]
                        existing_ids = existing_df[pk_column].tolist()
                        table_df = table_df[~table_df[pk_column].isin(existing_ids)]
                    else:
                        # Composite key: drop if all PK columns match
                        table_df = table_df.merge(
                            existing_df,
                            on=pk_columns,
                            how="left",
                            indicator=True
                        ).query("_merge == 'left_only'").drop(columns=["_merge"])

                    after_count = len(table_df)
                    logger.info(
                        f"Filtered {before_count - after_count} duplicate rows from {table}"
                    )

                if not table_df.empty:
                    table_df.to_sql(
                        name=table,
                        con=conn,
                        if_exists="append",
                        index=False,
                    )
                    logger.info(f">>>>> Successfully wrote data to {table} <<<<<")
                else:
                    logger.info(f"No new rows to insert into {table}")

        except Exception as inner_e:
            logger.error(f"Error while writing to DB: {inner_e}")
            return str(inner_e)

    except Exception as e:
        logger.error(f"Something went wrong:\n{traceback.format_exc()}")
        return str(e)

    return "Lambda finished successfully"

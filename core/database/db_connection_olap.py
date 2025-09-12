from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv(override=True)


def db_connection():
    return Connection(
        user=os.getenv("DB_OLAP_USERNAME"),
        password=os.getenv("DB_OLAP_PASSWORD"),
        database=os.getenv("DB_OLAP_DATABASE"),
        host=os.getenv("DB_OLAP_HOST"),
        port=os.getenv("DB_OLAP_PORT"),
        allow_multi_statements=True 
    )


def close_db(conn):
    conn.close()

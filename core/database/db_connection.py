from pg8000.native import Connection
from dotenv import load_dotenv
import os

load_dotenv(override=True)


def db_connection():
    return Connection(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )


def close_db(conn):
    conn.close()

from etl.database.db_connection import db_connection
from etl.utils.check_bucket_content import check_bucket_content
from etl.utils.insert_into_bucket import insert_into_bucket
from datetime import datetime, timedelta


def ingest_data(event, context):

    bucket_name = "etl-ingestion-bucket-2025"
    tables = []

    query_table_names = """
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE';"""

    conn = db_connection()
    
    tables.extend(conn.run(query_table_names))
    
    half_hour_before = datetime.now() - timedelta(minutes=30)
    time_now = datetime.now()
    
    for name in tables:
        query_retrieve_data = f"""
        SELECT * 
        FROM {name[0]}
        WHERE last_updated >= {half_hour_before 
         if check_bucket_content(bucket_name) else time_now}
        """

        print(query_retrieve_data)


    


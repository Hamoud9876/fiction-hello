from etl.database.db_connection_olap import db_connection
from etl.utils.check_bucket_content import check_bucket_content
from etl.utils.insert_into_bucket import insert_into_bucket
from datetime import datetime, timedelta
import io
import csv


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
    
    for table in tables:
        #retrieving table content
        query_retrieve_data = f"""
        SELECT * 
        FROM {table[0]}
        WHERE last_updated >= {half_hour_before 
         if check_bucket_content(bucket_name) else time_now}
        """

        table_content = conn.run(query_retrieve_data)

        #retrieving table columns headers
        table_headers = conn.run(
                f"""SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                AND table_name = '{table}';"""
            )

        #saving the content of the output in memory 
        #and tuning it to CSV format
        buffer = io.StringIO()
        writer = csv.write(buffer)
        writer.writerow(table_headers)
        writer.writerows(table_content)
        csv_content = buffer.getvalue()
        insert_into_bucket(bucket_name,table, csv_content)
        


    


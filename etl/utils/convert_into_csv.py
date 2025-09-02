import io
import csv
from etl.utils.insert_into_bucket import insert_into_bucket


def convert_into_csv(table, bucket_name, conn, query):

    table_content = conn.run(query)
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
    writer = csv.writer(buffer)
    writer.writerow([col[0] for col in table_headers])
    writer.writerows(table_content)
    csv_content = buffer.getvalue()
        
    insert_into_bucket(bucket_name, table, csv_content,"csv")
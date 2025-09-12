from etl.utils.get_bucket_dirs import get_bucket_dirs
from etl.utils.read_parquet_file import read_parquet_file
from etl.utils.load_into_olap import insert_df_into_db
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_load(event, context):
    """
    Loads files in processed bucjet to their destenation
    database.


    Args: 
        event: AWS required (not used)
        context: AWS required (not used)

    return: 
        dict: Status code 200 if loaded with no problems
    """

    bucket_name = "etl-process-bucket-2025"

    directories = get_bucket_dirs(bucket_name)
    timestamp = datetime.now()
    
    # Step 1: Read parquet
    for drictory in directories:
        df = read_parquet_file(bucket_name, timestamp,drictory)
    
        
        insert_df_into_db(df, drictory)

        logger.info(f"rows_inserted: {len(df)} in {drictory}")

    return {"status": 200}






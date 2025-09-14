from etl.database.db_connection_olap import db_connection
from etl.utils.check_bucket_content import check_bucket_content
from datetime import datetime, timedelta
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def ingest_data(event, context):
    """
    ingest the predefined tables and retrieve data based
    on if the bucket had been populated before or not,
    if yes will just pull data from the last 30 minutes
    else retrieve everything in the table

    reference tables get pulled fully all the
    time to maintain it consistentcy
    -----------------------------------------
    args:
    event: AWS required; not used
    context: AWS required; not used
    -----------------------------------------
    return: status code 200 if passing with no problems
    """
    from etl.utils.convert_to_csv import convert_to_csv

    bucket_name = "etl-ingestion-bucket-2025"

    tables = [
        "customers",
        "contracts",
        "contract_details",
        "customers_contracts",
        "contract_details_sims",
        "contracts_details_devices",
        "customers_usage",
        "customers_sims",
        "customers_address",
        "device_details",
        "billing",
        "sim_valid_history",
        "customer_status_history",
        "billing_status_history",
        "address",
        "charge_rates",
        "personal_data",
    ]

    ref_tables = [
        "pronounce",
        "genders",
        "contract_types",
        "contracts_periods",
        "sims",
        "sims_validation",
        "devices",
        "devices_types",
        "address_type",
        "customers_status",
        "billing_status",
    ]
    logging.info("started ingestion process")
    try:
        conn = db_connection()

        # checking if this is the first ever data pull or a normal 30 min
        half_hour_before = datetime.now() - timedelta(minutes=30)
        effective_time = (
            half_hour_before
            if check_bucket_content(bucket_name)
            else datetime(day=1, month=1, year=1954, hour=00, minute=00, second=00)
        )

        for table in tables:
            # retrieving table content
            query_normal = f"""
            SELECT * 
            FROM {table}
            WHERE last_updated >= '{effective_time}'
            """
            convert_to_csv(table, bucket_name, conn, query_normal)

        for ref_table in ref_tables:
            query_ref = f"""
            SELECT *
            FROM {ref_table}
            """
            convert_to_csv(ref_table, bucket_name, conn, query_ref)

    except Exception as e:
        logger.error(f"Somehing went wrong while ingesting data: {e}")
        return {"status": 400}

    logging.info(f"finished the ingestion process")
    return {"status": 200}

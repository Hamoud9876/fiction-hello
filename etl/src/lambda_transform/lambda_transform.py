from etl.utils.get_bucket_dirs import get_bucket_dirs
from etl.utils.get_latest_file import get_latest_file
from etl.utils.transform_dim_customers import transform_dim_customers
from etl.utils.transform_dim_contract import transform_dim_contract
from etl.utils.transform_dim_date import transform_dim_date
from etl.utils.transform_dim_location import transform_dim_location
from etl.utils.transform_customers_demo import transform_customers_demo
from etl.utils.transform_customers_usage import transform_customers_usage
from etl.utils.transform_billing import transform_billing
from etl.utils.transform_customers_contracts import transform_customers_contracts
from etl.utils.insert_into_bucket import insert_into_bucket
import io

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_transform(event, context):
    """
    transform the latest file in ingestion bucket,
    starts by retrieving the latest file in each directory,
    converting it to df then transform the df into their expected
    distenation structure
    -----------------------------------------
    args: 
    event: AWS required; not used
    context: AWS required; not used
    -----------------------------------------
    return: status code 200 if passing with no problems
    """

    bucket_name = "etl-ingestion-bucket-2025"
    bucket_processed = "etl-process-bucket-2025"
    directories = get_bucket_dirs(bucket_name)
    tables = {}
    olap_tables = {}

    try:
      logger.info("starting to retrieve latest files")
      for directory in directories:
         tables[directory]= get_latest_file(directory,bucket_name, bucket_processed) 

         
      logger.info("finished retrieving latest files")


      #transforming customers data to match dim_customers table structure
      olap_tables["dim_customers"] = transform_dim_customers(tables["customers"],
                              tables["genders"],
                              tables["pronounce"],
                              tables["customers_status"])
      

      #transforming contract data to match dim_contracts table structure
      olap_tables["dim_contract"] = transform_dim_contract(
         tables["contracts"],
         tables["contract_details"],
         tables["contracts_periods"],
         tables["contract_types"]
      )

      #transform address data to match dim_location table structure
      olap_tables["dim_location"] = transform_dim_location(
         tables["address"],
         tables["address_type"]
      )


      #transforming the date from all the tables to make sure no date is missing
      olap_tables["dim_date"] = transform_dim_date(
      customers=tables["customers"],
      contracts=tables["contracts"],
      contract_details=tables["contract_details"],
      customers_contracts=tables["customers_contracts"],
      # contract_details_sims=tables["contract_details_sims"],
      contracts_details_devices=tables["contracts_details_devices"],
      customers_usage=tables["customers_usage"],
      customers_sims=tables["customers_sims"],
      customers_address=tables["customers_address"],
      device_details=tables["device_details"],
      billing=tables["billing"],
      # sim_valid_history=tables["sim_valid_history"],
      customer_status_history=tables["customer_status_history"],
      billing_status_history=tables["billing_status_history"],
      address=tables["address"],
      # charge_rates=tables["charge_rates"],
      # personal_data=tables["personal_data"],
      genders=tables["genders"],
      contract_types=tables["contract_types"],
      contracts_periods=tables["contracts_periods"],
      sims=tables["sims"],
      sims_validation=tables["sims_validation"],
      devices=tables["devices"],
      devices_types=tables["devices_types"],
      address_type=tables["address_type"],
      customers_status=tables["customers_status"],
      billing_status=tables["billing_status"]
      )


      #transform customers location and their address history data to
      #create knowledge about where they are and track their changes
      olap_tables["fact_customers_demographic"] = transform_customers_demo(
         tables["customers_address"]
      )


      #transform customers usage data to match
      #fact_customers_usage table structure
      olap_tables["fact_customers_usage"] = transform_customers_usage(
         tables["customers_usage"]
      )

      
      #transform billing information data to create knowledge
      #about billing and track changes
      olap_tables["fact_billing"] = transform_billing(
         tables["billing"],
         tables["billing_status"]
      )

      #transform customers contract data to create knowledge
      #about customers contracts track changes
      olap_tables["fact_customers_contracts"] = transform_customers_contracts(
         tables["customers_contracts"],
         tables["contracts"],
         tables["contract_details"],
         tables["contracts_periods"],
      )


      #converting the content into parquet and inserting it
      #into the processed bucket
      for inx, df in olap_tables.items():
         logging.info(f"insert {inx} into proc bucket")
         
         #creating in-memory buffer
         buffer = io.BytesIO()

         #converting the dataframe into parquet
         df.to_parquet(buffer, engine="pyarrow", index=False)
         
         #moving the buffer cursor to the start
         buffer.seek(0)
         insert_into_bucket(bucket_processed,
         inx, 
         buffer,
         "parquet")

    except Exception as e:
       logging.error(f"Something went wrong: {e}")
       return {"status": 400}
    
    return {"status": 200}
    
from core.src.generate_customers_data import generate_customers_data
from core.src.customers_status_data import customers_status_data
from core.src.generate_address_data import generate_address_data
from core.src.generate_contracts import generate_contracts
from core.src.generate_sim_data import generate_sims_data
from core.database.core_tables import create_tables
from core.database.insert_tables import insert_tables
from core.src.customer_usage import customer_usage
from core.src.generate_billings import generate_bellings
from core.database.create_olap_db import create_olap_db
from core.exceptions.invalid_input_exception import InvalidInput
import logging


logging.basicConfig(
    filename="app_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main(num_cust):
    customers = {"customers": generate_customers_data(num_cust)}

    for i in customers["customers"]:
        try:
            i["cust_status"] = customers_status_data(i["join_date"])
            i["cust_address"] = generate_address_data()
            i["con_details"] = generate_contracts(1, 1, i["cust_status"])
            i["usage"] = []
            i["billing"] = []
            sims_num = 0
            for y in i["con_details"]:
                if y["num_of_sims"] > sims_num:
                    sims_num = y["num_of_sims"]
            i["sims"] = generate_sims_data(sims_num)
            for y in i["con_details"]:
                if y["contract_title"] != "pgo":
                    placeholder_usage = customer_usage(y["con_period"], y["start_date"])
                    i["billing"].extend(
                        generate_bellings(placeholder_usage, y["price"])
                    )
                    i["usage"].extend(placeholder_usage)

        except InvalidInput as e:
            logging.error(str(e.value))
    create_tables()
    insert_tables(customers)
    create_olap_db()

from core.src.generate_customers_data import generate_customers_data
from core.src.customers_status_data import customers_status_data
from core.src.generate_address_data import generate_address_data
from core.src.generate_contracts import generate_contracts
from core.src.generate_sim_data import generate_sims_data
from core.database.core_tables import create_tables
from core.database.insert_tables import insert_tables


def main(num_cust):
    customers = {"customers": generate_customers_data(num_cust)}

    for i in customers["customers"]:
        i["cust_status"] = customers_status_data(i["join_date"])
        i["cust_address"] = generate_address_data()
        i["con_details"] = generate_contracts(1, 1, i["cust_status"])
        sims_num = 0
        for y in i["con_details"]:
            if y["num_of_sims"] > sims_num:
                sims_num = y["num_of_sims"]
        i["sims"] = generate_sims_data(sims_num)
    create_tables()
    insert_tables(customers)

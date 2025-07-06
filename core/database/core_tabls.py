from db_connection import Connection, close_db


def create_tables():
    conn = Connection()

    query = """TABLE genders(
  gender_id SERIAL PRIMARY KEY,
  gender_title varchar(200)
)
"""
    conn.run(query)

    query = """TABLE pronounce(
  pronuonce_id SERIAL PRIMARY KEY,
  pronounce_title varchar(100)
)"""
    conn.run(query)

    query = """TABLE customers(
    customer_id SERIAL PRIMARY KEY,
    first_name varchar(100),
    middle_name varchar(100),
    last_name varchar(100),
    birthdate date,
    join_date datetime,
    gender_id int REFERENCES genders(gender_id)
    pronuonce int REFERENCES pronounce_types,
    customer_status_id int REFERENCES customers_status(customer_status_id),
    )
    """
    conn.run(query)

    query = """TABLE contract_types(
            contract_type_id SERIAL PRIMARY KEY,
            contract_type varchar(100),
            )
    """
    conn.run(query)

    query = """TABLE contract_details(
            contract_details_id SERIAL PRIMARY KEY,
            contract_title varchar(300),
            initial_price decimal(12,2),
            discount_percent decimal(4,1),
            period int,
            num_of_sims int,
            num_of_devices int,
            created_at datetime,
            last_updated datetime,
            )
    """
    conn.run(query)

    query = """TABLE contracts(
contract_id SERIAL PRIMARY KEY,
contract_details_id int REFERENCES contract_details(contract_details_id),
contract_type_id int REFERENCES contract_types(contract_type_id),
created_at datetime,
last_updated datetime,
)
    """
    conn.run(query)

    query = """TABLE customers_contracts(
            customer_contract_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            contract_id int REFERENCES contracts(contract_id),
            )
    """
    conn.run(query)

    query = """TABLE sims(
                sim_id SERIAL PRIMARY KEY,
                avail_calls_time int,
                avail_cellular_data decimal(12,2),
                avail_roam_data decimal(12,2),
                avail_roam_calls_time int,
                created_at datetime,
                last_updated datetime,
                )
    """
    conn.run(query)

    query = """TABLE contract_details_sims{
        con_detail_sims_id SERIAL PRIMARY KEY,
contract_details_id int REFERENCES contract_details(contract_details_id),
        sim_id int REFERENCES sims(sim_id)
}
"""
    conn.run(query)

    query = """TABLE devices_type{
            devices_type_id SERIAL PRIMARY KEY,
            device_type varchar(100),
            }
    """
    conn.run(query)

    query = """TABLE devices_details(
            devices_details_id SERIAL PRIMARY KEY,
            device_model varchar(100),
            company varchar(100),
            screen_size decimal(4,1),
            ram int,
            storage int,
            )
    """
    conn.run(query)

    query = """TABLE devices()
device_id SERIAL PRIMARY KEY,
device_name varchar(200),
contract_details_id int REFERENCES contract_details(contract_details_id),
device_type_id int REFERENCES devices_type(devices_type_id),
device_details_id int REFERENCES devices_details(devices_details_id),
created_at datetime,
last_updated datetime,
)
    """
    conn.run(query)

    query = """TABLE customers_usage(
            customer_usage_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            used_cellular_data decimal(12,2),
            used_call_time int,
            used_roam_data decimal(12,2),
            used_roam_call_time int,
            start_date datetime,
            end_date datetime,
            )
    """
    conn.run(query)

    query = """TABLE customers_sims{
            customer_sim_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            sims_id int REFERENCES sims(sim_id),
            }
    """
    conn.run(query)

    query = """TABLE address_type(
            address_type_id SERIAL PRIMARY KEY,
            address_type varchar(30),
            )
    """
    conn.run(query)

    query = """TABLE address(
            address_id SERIAL PRIMARY KEY,
            first_line varchar(200),
            second_line varchar(200),
            city varchar(200),
            county varchar(200),
            post_code varchar(200),
            address_type_id int REFERENCES address_type(address_type_id),
            start_date datetime,
            end_date datetime,
            )
    """
    conn.run(query)

    query = """TABLE customers_address(
            customers_address_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            address_id int REFERENCES address(address_id),
            )
    """
    conn.run(query)

    query = """TABLE customers_status()
            customer_status_id SERIAL PRIMARY KEY,
            status varchar(30),
            )
    """
    conn.run(query)

    query = """TABLE customer_status_history()
customer_status_history_id SERIAL PRIMARY KEY,
customer_status_id int REFERENCES customers_status(customer_status_id),
customer_id int REFERENCES customers(customer_id),
change_date datetime,
)
    """
    conn.run(query)

    query = """TABLE billing_status()
            bill_status_id SERIAL PRIMARY KEY,
            status varchar(30),
            )
    """
    conn.run(query)

    query = """TABLE billing(
            bill_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            contract_id int REFERENCES contracts(contract_id),
            amount decimal(10,2),
            bill_status_id int REFERENCES billing_status(bill_status_id),
            issue_date datetime,
            completed_date datetime,
            due_date datetime,
            )
    """
    conn.run(query)

    query = """TABLE billing_status_history(
            billing_status_history_id SERIAL PRIMARY KEY,
            bill_id int REFERENCES billing(bill_id),
            bill_status_id int REFERENCES billing_status(bill_status_id),
            change_date datetime,
            )
    """
    conn.run(query)

    query = """TABLE charge_rates(
            charge_rate_id SERIAL PRIMARY KEY,
            call_minute_rate decimal(5,2),
            data_mp_rate decimal(5,2),
            roam_call_minute_rate decimal(5,2),
            roam_data_mp_rate decimal(5,2),
            start_date datetime,
            end_date datetime,
            )
    """
    conn.run(query)

    close_db(conn)

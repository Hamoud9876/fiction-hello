from core.database.db_connection import db_connection, close_db


def create_tables():
    conn = db_connection()

    query = """
    CREATE TABLE IF NOT EXISTS genders(
  gender_id SERIAL PRIMARY KEY,
  gender_title varchar(200) UNIQUE,
  created_at timestamp,
  last_updated timestamp
);
"""
    conn.run(query)

    query = """
    CREATE TABLE IF NOT EXISTS pronounce(
  pronounce_id SERIAL PRIMARY KEY,
  pronounce_title varchar(100) UNIQUE,
  created_at timestamp,
  last_updated timestamp
);"""
    conn.run(query)

    query = """
    CREATE TABLE IF NOT  EXISTS customers_status(
            customer_status_id SERIAL PRIMARY KEY,
            status varchar(30) UNIQUE,
            created_at timestamp,
            last_updated timestamp
            );
    """
    conn.run(query)

    query = """
    CREATE TABLE IF NOT EXISTS customers(
    customer_id SERIAL PRIMARY KEY,
    first_name varchar(100),
    middle_name varchar(100),
    last_name varchar(100),
    birthdate date,
    join_date timestamp,
    gender_id int REFERENCES genders(gender_id),
    pronounce_id int REFERENCES pronounce(pronounce_id),
    customer_status_id int REFERENCES customers_status(customer_status_id),
    last_updated timestamp
    );
    """
    conn.run(query)

    query = """
    CREATE TABLE IF NOT EXISTS customer_status_history(
customer_status_history_id SERIAL PRIMARY KEY,
customer_status_id int REFERENCES customers_status(customer_status_id),
customer_id int REFERENCES customers(customer_id),
change_date timestamp,
created_at timestamp,
last_updated timestamp
);
    """
    conn.run(query)

    query = """
    CREATE TABLE IF NOT EXISTS contract_types(
            contract_type_id SERIAL PRIMARY KEY,
            contract_type varchar(100) UNIQUE,
            created_at timestamp,
  last_updated timestamp
            )
    """
    conn.run(query)

    query = """
    CREATE TABLE IF NOT EXISTS contracts_periods(
        contract_period_id SERIAL PRIMARY KEY,
        period int UNIQUE,
        created_at timestamp,
  last_updated timestamp
       );
       """
    conn.run(query)

    query = """
CREATE TABLE IF NOT EXISTS sims_validation(
validation_id SERIAL PRIMARY KEY,
validation varchar(20) UNIQUE,
created_at timestamp,
last_updated timestamp
);
"""
    conn.run(query)
    query = """CREATE TABLE IF NOT EXISTS sims(
                sim_id SERIAL PRIMARY KEY,
                number int,
validation_id int REFERENCES sims_validation(validation_id),
                created_at timestamp,
                last_updated timestamp
                );
    """
    conn.run(query)

    query = """
CREATE TABLE IF NOT EXISTS sim_valid_history(
sim_valid_hist_id SERIAL PRIMARY KEY,
validation_id int REFERENCES sims_validation(validation_id),
change_date timestamp,
created_at timestamp,
last_updated timestamp
);
"""
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS personal_data(
    personal_data_id SERIAL PRIMARY KEY,
  sim_id int REFERENCES sims(sim_id),
  avail_calls_time int,
  avail_cellular_data decimal(12,2),
  avail_roam_data decimal(12,2),
  avail_roam_calls_time int,
  start_date timestamp,
  end_date timestamp,
  created_at timestamp,
  last_updated timestamp
    );
"""

    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS contract_details(
            contract_details_id SERIAL PRIMARY KEY,
            contract_title varchar(300),
            initial_price decimal(12,2),
            discount_percent decimal(4,1),
contract_period_id int REFERENCES contracts_periods(contract_period_id),
            num_of_sims int,
            num_of_devices int,
            personal_data_id int REFERENCES personal_data(personal_data_id),
            created_at timestamp,
            last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS contracts(
contract_id SERIAL PRIMARY KEY,
contract_details_id int REFERENCES contract_details(contract_details_id),
contract_type_id int REFERENCES contract_types(contract_type_id),
created_at timestamp,
last_updated timestamp
);
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS customers_contracts(
            customer_contract_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            contract_id int REFERENCES contracts(contract_id),
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS contract_details_sims(
        con_detail_sims_id SERIAL PRIMARY KEY,
contract_details_id int REFERENCES contract_details(contract_details_id),
        sim_id int REFERENCES sims(sim_id),
        created_at timestamp,
  last_updated timestamp
);
"""
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS devices_types(
            device_type_id SERIAL PRIMARY KEY,
            device_type varchar(100) UNIQUE,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS devices_details(
            devices_details_id SERIAL PRIMARY KEY,
            device_model varchar(100),
            company varchar(100),
            screen_size decimal(4,1),
            ram int,
            storage int,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """ CREATE TABLE IF NOT EXISTS devices(
device_id SERIAL PRIMARY KEY,
model varchar(200),
brand varchar(200),
device_type_id int REFERENCES devices_types(device_type_id),
created_at timestamp,
last_updated timestamp
);
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS device_details(
  device_detail_id SERIAL PRIMARY KEY,
  device_id int REFERENCES devices(device_id),
  screen_size decimal(4,1),
  ram int,
  storage int,
  price decimal(12,2),
  discount_percent int,
  created_at timestamp,
  last_updated timestamp
);
"""
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS contracts_details_devices(
  con_details_dev_id SERIAL PRIMARY KEY,
  contract_details_id int REFERENCES contract_details(contract_details_id),
  device_id int REFERENCES devices(device_id),
  created_at timestamp,
  last_updated timestamp
);"""
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS contracts_details_sims(
  con_detail_sims_id SERIAL PRIMARY KEY,
  contract_details_id int REFERENCES contract_details(contract_details_id),
  sim_id int REFERENCES sims(sim_id),
  created_at timestamp,
  last_updated timestamp
)
"""

    query = """CREATE TABLE IF NOT EXISTS customers_usage(
            customer_usage_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            used_cellular_data decimal(12,2),
            used_call_time int,
            used_roam_data decimal(12,2),
            used_roam_call_time int,
            start_date timestamp,
            end_date timestamp,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS customers_sims(
            customer_sim_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            sim_id int REFERENCES sims(sim_id),
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS address_type(
            address_type_id SERIAL PRIMARY KEY,
            address_type varchar(30) UNIQUE,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS address(
            address_id SERIAL PRIMARY KEY,
            first_line varchar(200),
            second_line varchar(200),
            city varchar(200),
            county varchar(200),
            post_code varchar(200),
            address_type_id int REFERENCES address_type(address_type_id),
            start_date timestamp,
            end_date timestamp,
            created_at timestamp,
            last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS customers_address(
            customers_address_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            address_id int REFERENCES address(address_id),
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS billing_status(
            bill_status_id SERIAL PRIMARY KEY,
            status varchar(30) UNIQUE,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS billing(
            bill_id SERIAL PRIMARY KEY,
            customer_id int REFERENCES customers(customer_id),
            contract_id int REFERENCES contracts(contract_id),
            amount decimal(10,2),
            bill_status_id int REFERENCES billing_status(bill_status_id),
            issue_date timestamp,
            completed_date timestamp,
            due_date timestamp,
            created_at timestamp,
        last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS billing_status_history(
            billing_status_history_id SERIAL PRIMARY KEY,
            bill_id int REFERENCES billing(bill_id),
            bill_status_id int REFERENCES billing_status(bill_status_id),
            change_date timestamp,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    query = """CREATE TABLE IF NOT EXISTS charge_rates(
            charge_rate_id SERIAL PRIMARY KEY,
            call_minute_rate decimal(5,2),
            data_mp_rate decimal(5,2),
            roam_call_minute_rate decimal(5,2),
            roam_data_mp_rate decimal(5,2),
            start_date timestamp,
            end_date timestamp,
            created_at timestamp,
  last_updated timestamp
            );
    """
    conn.run(query)

    close_db(conn)

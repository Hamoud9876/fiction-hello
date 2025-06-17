

def create_tables():
    """CREATE TABLE customers(
            customer_id SERIAL PRIMARY KEY,
            first_name varchar(20),
            middle_name varchar(20),
            last_name varchar(30),
            join_date date,
            status varchar(20),
            contract_id int REFERENCES contracts(contract_id)
    )
    """

    """CREATE TABLE contract_details(
            contract_details_id SERIAL PRIMARY KEY,
            contract_price float,
            contract_period int,
            calls_minutes int,
            cellular_data int,
            roam_data int,
            roam_calls_minutes int
    )"""

    """CREATE TABLE contracts(
            contract_id SERIAL PRIMARY KEY,
            contract_name varchar,
            contract_details_id int REFERENCES contract_details(contract_details_id)
     )"""
    

    
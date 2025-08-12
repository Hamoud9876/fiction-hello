from core.data.data import genders
from core.data.data import pronounce
from core.data.data import customers_status
from core.data.data import periods
from core.data.data import address_type
from core.data.data import contract_type
from core.data.data import devices
from core.data.data import billing_status
from core.database.db_connection import db_connection, close_db
from datetime import datetime


def insert_tables(customers: dict):
    conn = db_connection()

    created_date = datetime(day=1,month=1,year=1954,hour=00,minute=00,second=00)
 

    query = """INSERT INTO genders(gender_title,
    created_at, last_updated)
    VALUES (:gender_title,:created_at,:last_updated)
    ON CONFLICT (gender_title) DO NOTHING;"""

    for gender in genders:
        conn.run(query, gender_title=gender,
                 created_at=created_date,
                 last_updated=created_date )


    query = """INSERT INTO pronounce(pronounce_title,
      created_at, last_updated)
    VALUES(:pronounce_title, :created_at,:last_updated)
    ON CONFLICT (pronounce_title) DO NOTHING;"""

    for pronoun in pronounce:
        conn.run(query, pronounce_title=pronoun,
                 created_at=created_date,
                 last_updated=created_date )


    query = """INSERT INTO customers_status(status,
    created_at, last_updated)
    VALUES(:status, :created_at,:last_updated)
    ON CONFLICT (status) DO NOTHING;"""

    for status in customers_status:
        conn.run(query, status=status,
                 created_at=created_date,
                 last_updated=created_date)


    query = """INSERT INTO contracts_periods(period,
    created_at, last_updated)
    VALUES(:period, :created_at,:last_updated)
    ON CONFLICT (period) DO NOTHING;"""

    for period in periods:
        conn.run(query, period=period,
                 created_at=created_date,
                 last_updated=created_date)


    query = """INSERT INTO address_type(address_type,
    created_at, last_updated)
    VALUES(:address_type, :created_at, :last_updated)
    ON CONFLICT (address_type) DO NOTHING;"""

    for address in address_type:
        conn.run(query, address_type=address,
                 created_at=created_date,
                 last_updated=created_date)


    query = """INSERT INTO contract_types(contract_type,
    created_at, last_updated)
    VALUES(:contract_type, :created_at, :last_updated)
    ON CONFLICT (contract_type) DO NOTHING;"""


    for contract in contract_type:
        conn.run(query, contract_type=contract,
                 created_at=created_date,
                 last_updated=created_date)

    query = """INSERT INTO devices_types(device_type,
    created_at, last_updated)
    VALUES(:device_type,:created_at, :last_updated)
    ON CONFLICT (device_type) DO NOTHING;"""


    for device in devices:
        conn.run(query, device_type=device,
                 created_at=created_date,
                 last_updated=created_date)


    for customer in customers["customers"]:
        query = """INSERT INTO customers(
        first_name, middle_name,last_name,birthdate, gender_id,
        pronounce_id, customer_status_id, join_date,last_updated)
        VALUES (:first_name, :middle_name, :last_name, :birthdate, :gender_id,
        :pronounce_id, :customer_status_id, :join_date,:last_updated)
        RETURNING customer_id;"""

        cust_id = conn.run(
            query,
            first_name=customer["first_name"],
            middle_name=customer["middle_name"],
            last_name=customer["last_name"],
            birthdate=customer["birthdate"],
            gender_id=customer["gender"] + 1,
            pronounce_id=customer["pronounce"] + 1,
            customer_status_id=customers_status.index(
                customer["cust_status"]["customer_status"]
            )
            + 1,
            join_date=customer["join_date"],
            last_updated=customer["join_date"],
        )[0][0]

        query_usage = """INSERT INTO customers_usage(
        customer_id, used_cellular_data, used_call_time,
        used_roam_data, used_roam_call_time, start_date, end_date
        ,created_at,last_updated
        )
        VALUES(
        :customer_id, :used_cellular_data, :used_call_time,
        :used_roam_data, :used_roam_call_time, :start_date, :end_date,
        :created_at,:last_updated
        );
        """

        for usage_record in customer["usage"]:
            conn.run(
                query_usage,
                customer_id=cust_id,
                used_cellular_data=usage_record["used_cellular_data"],
                used_call_time=usage_record["used_call_time"],
                used_roam_data=usage_record["used_roam_data"],
                used_roam_call_time=usage_record["used_roam_call_time"],
                start_date=usage_record["start_date"],
                end_date=usage_record["end_date"],
                created_at=usage_record["start_date"],
                last_updated=usage_record["start_date"]
            )

        query = """INSERT INTO address(
        first_line, second_line, city, county, post_code,
        address_type_id, start_date, created_at, last_updated)
        VALUES(:first_line, :second_line, :city, :county, :post_code,
        :address_typ_id, :start_date, :created_at, :last_updated)
        RETURNING address_id;"""

        for address in customer["cust_address"]:
            address_id = conn.run(
                query,
                first_line=address["first_line"],
                second_line=address["second_line"],
                city=address["city"],
                county=address["county"],
                post_code=address["post_code"],
                address_typ_id=address_type.index(address["address_type"]) + 1,
                start_date=customer["join_date"],
                created_at=customer["join_date"],
                last_updated=customer["join_date"],
            )[0][0]

            query_cust_add = """
            INSERT INTO customers_address(customer_id, address_id)
        VALUES(:cust_id,:address_id);"""

            conn.run(query_cust_add, cust_id=cust_id, address_id=address_id)

        query = """INSERT INTO sims(number, created_at, last_updated)
            VALUES(:number, :created_at,:last_updated)
            RETURNING sim_id;"""
        sims_ids = []
        for sim in customer["sims"]:

            sims_ids.append(
                conn.run(
                    query,
                    number=sim,
                    created_at=customer["join_date"],
                    last_updated=customer["join_date"],
                )[0][0]
            )

        query_cust_sims = """INSERT INTO customers_sims(customer_id, sim_id, created_at, last_updated)
        VALUES(:customer_id,:sim_id, :created_at,:last_updated);"""

        for i in sims_ids:
            conn.run(query_cust_sims, customer_id=cust_id, sim_id=i,
                     created_at=created_date,
                     last_updated=created_date)

        query_con_details = """INSERT INTO contract_details(
        contract_title, initial_price, discount_percent,contract_period_id,
        num_of_sims,num_of_devices, personal_data_id, created_at, last_updated)
        VALUES(:contract_title, :initial_price, :discount_percent,
        :contract_period_id, :num_of_sims, :num_of_devices, :personal_data_id,
        :created_at, :last_updated)
        RETURNING contract_details_id;"""

        query_per_data = """INSERT INTO personal_data(avail_calls_time,
        avail_cellular_data, avail_roam_data, avail_roam_calls_time,
        start_date, end_date, created_at, last_updated)
        VALUES(:avail_call_time,:avail_cellular_data,:avail_roam_data
        ,:avail_roam_calls_time,:start_date,:end_date, :created_at, :last_updated)
        RETURNING personal_data_id;"""

        query_devices = """INSERT INTO devices(
        model, brand, device_type_id, created_at, last_updated)
        VALUES(:model,:brand,:devic_typ_id,:created_at,:last_updated)
        RETURNING device_id;"""

        query_devices_details = """INSERT INTO device_details(
        device_id, screen_size, ram, storage, price, discount_percent
        ,created_at, last_updated)
        VALUES (
        :device_id, :screen_size, :ram, :storage, :price, :discount_percent
        ,:created_at, :last_updated);"""

        for con in customer["con_details"]:
            personal_data = conn.run(
                query_per_data,
                avail_call_time=con["available_data"]["calls_times"],
                avail_cellular_data=con["available_data"]["cellular_data"],
                avail_roam_data=con["available_data"]["roam_data"],
                avail_roam_calls_time=con["available_data"]["roam_call_time"],
                start_date=customer["join_date"],
                end_date=customer["join_date"],
                created_at=customer["join_date"],
                last_updated=customer["join_date"]
            )[0][0]

            con_details = conn.run(
                query_con_details,
                contract_title=con["contract_title"],
                initial_price=con["price"],
                discount_percent=0,
                contract_period_id=periods.index(con["con_period"]) + 1,
                num_of_sims=con["num_of_sims"],
                num_of_devices=con["num_of_devices"],
                personal_data_id=personal_data,
                created_at=customer["join_date"],
                last_updated=customer["join_date"],
            )[0][0]

            devices_ids = []
            if con["devices"] != 0:
                for dev in con["devices"]:
                    devices_ids.append(
                        conn.run(
                            query_devices,
                            model=dev["device_model"],
                            brand=dev["company"],
                            devic_typ_id=devices.index(dev["device_type"]) + 1,
                            created_at=customer["join_date"],
                            last_updated=customer["join_date"],
                        )[0][0]
                    )

                    conn.run(
                        query_devices_details,
                        device_id=devices_ids[-1],
                        screen_size=dev["screen_size"],
                        ram=dev["ram"],
                        storage=dev["storage"],
                        price=dev["price"],
                        discount_percent=0,
                        created_at=customer["join_date"],
                        last_updated=customer["join_date"],
                    )

            query_dev_id_con_det_id = """INSERT INTO contracts_details_devices(
            contract_details_id, device_id, created_at, last_updated)
            VALUES(:contract_details_id, :device_id, :created_at, :last_updated);"""
            for dev_id in devices_ids:
                conn.run(
                    query_dev_id_con_det_id,
                    contract_details_id=con_details,
                    device_id=dev_id,
                    created_at=customer["join_date"],
                    last_updated=customer["join_date"]
                )

            query_contracts = """INSERT INTO contracts(
            contract_details_id, contract_type_id, created_at,
            last_updated
            )
            VALUES(
            :contract_details_id, :contract_type_id, :created_at,
            :last_updated
            )
            RETURNING contract_id;
            """

            con_id = conn.run(
                query_contracts,
                contract_details_id=con_details,
                contract_type_id=(1 if con["con_period"] == 0 else 2),
                created_at=customer["join_date"],
                last_updated=customer["join_date"],
            )[0][0]

            query_cust_con = """INSERT INTO customers_contracts(
            customer_id, contract_id, created_at, last_updated)
            VALUES(:customer_id, :contract_id, :created_at, :last_updated);"""

            conn.run(query_cust_con,
                     customer_id=cust_id,
                     contract_id=con_id,
                     created_at=customer["join_date"] ,
                     last_updated=customer["join_date"])

            query_billing_status = """INSERT INTO billing_status(
            status, created_at, last_updated
            )
            VALUES(:status, :created_at, :last_updated)
            ON CONFLICT (status) DO NOTHING
            """
            for status in billing_status:
                conn.run(query_billing_status, status=status,
                         created_at=customer["join_date"],
                         last_updated=customer["join_date"])

            query_billing = """INSERT INTO billing(
            customer_id, contract_id, amount, bill_status_id, issue_date,
            completed_date, due_date, created_at, last_updated
            )
            VALUES (
            :customer_id, :contract_id, :amount, :bill_status_id, :issue_date,
            :completed_date, :due_date, :created_at, :last_updated
            )"""
            for bill in customer["billing"]:
                print(bill)
                conn.run(
                    query_billing,
                    customer_id=cust_id,
                    contract_id=con_id,
                    amount=bill["amount"],
                    bill_status_id=1 if bill["status"] == "Paid" else 2,
                    issue_date=bill["issue_date"],
                    completed_date=bill["complete_date"],
                    due_date=bill["due_date"],
                    created_at=bill["issue_date"],
                    last_updated=bill["issue_date"]
                )

    close_db(conn)

import textwrap
from core.database.db_connection_olap import db_connection, close_db


def create_olap_db():
    conn = db_connection()

    query_create_olap_tables = textwrap.dedent(
        """
        CREATE TABLE IF NOT EXISTS dim_contract (
            contract_id      INT PRIMARY KEY NOT NULL,
            contract_title   VARCHAR(300) NOT NULL,
            contract_type    VARCHAR(100) NOT NULL,
            initial_price    DECIMAL(12,2) NOT NULL,
            discount_percent INT NOT NULL,
            effective_price  DECIMAL(12,2) NOT NULL,
            contract_period  INT NOT NULL,
            num_of_sims      INT NOT NULL,
            num_of_devices   INT NOT NULL,
            personal_data_id INT NOT NULL
                REFERENCES dim_personal_data (personal_data_id)
        );

        CREATE TABLE IF NOT EXISTS dim_locations (
            location_id   INT PRIMARY KEY NOT NULL,
            full_address  VARCHAR(300) NOT NULL,
            city          VARCHAR(200) NOT NULL,
            county        VARCHAR(200) NOT NULL,
            post_code     VARCHAR(200) NOT NULL,
            address_type  VARCHAR(30) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_customers (
            customer_id     INT PRIMARY KEY NOT NULL,
            full_name       VARCHAR(300) NOT NULL,
            gender          VARCHAR(200) NOT NULL,
            pronoun         VARCHAR(200) NOT NULL,
            join_date       DATE NOT NULL,
            customer_status VARCHAR(100) NOT NULL,
            age             INT NOT NULL,
            age_group       VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_sims (
            sim_id INT PRIMARY KEY NOT NULL,
            number INT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_date (
            date_id     DATE PRIMARY KEY NOT NULL,
            day         INT NOT NULL,
            month       INT NOT NULL,
            year        INT NOT NULL,
            day_of_week INT NOT NULL,
            day_name    VARCHAR(20) NOT NULL,
            month_name  VARCHAR(20) NOT NULL,
            quarter     INT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_device (
            device_id       INT PRIMARY KEY NOT NULL,
            model           VARCHAR(200) NOT NULL,
            brand           VARCHAR(200) NOT NULL,
            device_type     VARCHAR(100) NOT NULL,
            screen_size     DECIMAL(4,1) NOT NULL,
            ram             INT NOT NULL,
            storage         INT NOT NULL,
            retail_price    FLOAT NOT NULL,
            discount_percent INT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_personal_data (
            personal_data_id   INT PRIMARY KEY NOT NULL,
            avail_calls_time   INT,
            avail_cellular_data DECIMAL(12,2),
            avail_roam_data    DECIMAL(12,2),
            avail_roam_calls_time INT,
            start_date         TIMESTAMP,
            end_date           TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS fact_customers_contracts (
            contract_record SERIAL PRIMARY KEY,
            customer_id     INT NOT NULL
                REFERENCES dim_customers (customer_id),
            contract_id     INT NOT NULL
                REFERENCES dim_contract (contract_id),
            start_date      DATE NOT NULL
                REFERENCES dim_date (date_id),
            end_date        DATE NOT NULL
                REFERENCES dim_date (date_id),
            is_active       BOOL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS fact_customers_demographic (
            demographic_record SERIAL PRIMARY KEY,
            customer_id        INT NOT NULL
                REFERENCES dim_customers (customer_id),
            location_id        INT NOT NULL
                REFERENCES dim_locations (location_id),
            date_id            DATE NOT NULL
                REFERENCES dim_date (date_id)
        );

        CREATE TABLE IF NOT EXISTS fact_customers_usage (
            customer_usage_id  SERIAL PRIMARY KEY,
            customer_id        INT NOT NULL
                REFERENCES dim_customers (customer_id),
            used_cellular_data DECIMAL(12,2) NOT NULL,
            used_call_time     INT NOT NULL,
            used_roam_call_time INT NOT NULL,
            used_roam_data     DECIMAL(12,2) NOT NULL,
            start_date         DATE NOT NULL,
            end_date           DATE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS fact_billing (
            billing_id    SERIAL PRIMARY KEY,
            customer_id   INT NOT NULL
                REFERENCES dim_customers (customer_id),
            contract_id   INT NOT NULL
                REFERENCES dim_contract (contract_id),
            amount_billed DECIMAL(10,2) NOT NULL,
            amount_paid   DECIMAL(10,2) NOT NULL,
            is_paid       BOOL NOT NULL,
            days_overdue  INT NOT NULL,
            bill_status   VARCHAR NOT NULL,
            issue_date    DATE NOT NULL
                REFERENCES dim_date (date_id),
            complete_date DATE NOT NULL
                REFERENCES dim_date (date_id),
            due_date      DATE NOT NULL
                REFERENCES dim_date (date_id),
            created_at    DATE NOT NULL
                REFERENCES dim_date (date_id),
            last_updated  DATE NOT NULL
                REFERENCES dim_date (date_id)
        );
    """
    )

    conn.run(query_create_olap_tables)
    close_db(conn)

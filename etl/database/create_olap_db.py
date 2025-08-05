from etl.database.db_connection import db_connection, close_db

def create_olap_db():
    conn = db_connection()

    query_create_olap_tables = """CREATE TABLE "dim_contract" (
  "contract_id" int PRIMARY KEY NOT NULL,
  "contract_title" varchar(300) NOT NULL,
  "contract_type" varchar(100) NOT NULL,
  "initial_price" decimal(12,2) NOT NULL,
  "discount_percent" int NOT NULL,
  "effective_price" decimal(12,2) NOT NULL,
  "contract_period" int NOT NULL,
  "num_of_sims" int NOT NULL,
  "num_of_devices" int NOT NULL,
  "personal_data_id" int NOT NULL
);

CREATE TABLE "dim_locations" (
  "location_id" int PRIMARY KEY NOT NULL,
  "full_address" varchar(300) NOT NULL,
  "city" varchar(200) NOT NULL,
  "county" varchar(200) NOT NULL,
  "post_code" varchar(200) NOT NULL,
  "address_type" varchar(30) NOT NULL
);

CREATE TABLE "dim_customers" (
  "customer_id" int PRIMARY KEY NOT NULL,
  "full_name" varchar(300) NOT NULL,
  "gender" varchar(200) NOT NULL,
  "pronoun" varchar(200) NOT NULL,
  "join_date" date NOT NULL,
  "age" int NOT NULL,
  "age_group" varchar(100) NOT NULL
);

CREATE TABLE "dim_sims" (
  "sim_id" int PRIMARY KEY NOT NULL,
  "number" int NOT NULL
);

CREATE TABLE "dim_date" (
  "date_id" date PRIMARY KEY NOT NULL,
  "day" int NOT NULL,
  "month" int NOT NULL,
  "year" int NOT NULL,
  "day_of_week" int NOT NULL,
  "day_name" varchar(20) NOT NULL,
  "month_name" varchar(20) NOT NULL,
  "quarter" int NOT NULL
);

CREATE TABLE "dim_device" (
  "device_id" int PRIMARY KEY NOT NULL,
  "model" varchar(200) NOT NULL,
  "brand" varchar(200) NOT NULL,
  "device_type" varchar(100) NOT NULL,
  "screen_size" decimal(4,1) NOT NULL,
  "ram" int NOT NULL,
  "storage" int NOT NULL,
  "retail_price" float NOT NULL,
  "discount_percent" int NOT NULL
);

CREATE TABLE "dim_personal_data" (
  "personal_data_id" int PRIMARY KEY NOT NULL,
  "avail_calls_time" int,
  "avail_cellular_data" decimal(12,2),
  "avail_roam_data" decimal(12,2),
  "avail_roam_calls_time" int,
  "start_date" timestamp,
  "end_date" timestamp
);

CREATE TABLE "fact_customers_contracts" (
  "contract_record" SERIAL PRIMARY KEY,
  "customer_id" int NOT NULL,
  "contract_id" int NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date NOT NULL,
  "is_active" bool NOT NULL
);

CREATE TABLE "fact_customers_demographic" (
  "demographic_record" SERIAL PRIMARY KEY,
  "customer_id" int NOT NULL,
  "location_id" int NOT NULL,
  "date_id" date NOT NULL
);

CREATE TABLE "fact_customers_usage" (
  "customer_usage_id" SERIAL PRIMARY KEY,
  "customer_id" int NOT NULL,
  "used_cellular_data" decimal(12,2) NOT NULL,
  "used_call_time" int NOT NULL,
  "used_roam_call_time" int NOT NULL,
  "used_roam_data" decimal(12,2) NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date NOT NULL
);

CREATE TABLE "fact_billing" (
  "billing_id" SERIAL PRIMARY KEY,
  "customer_id" int NOT NULL,
  "contract_id" int NOT NULL,
  "amount_billed" decimal(10,2) NOT NULL,
  "ammount_paid" decimal(10,2) NOT NULL,
  "is_paid" bool NOT NULL,
  "days_overdue" int NOT NULL,
  "bill_status" varchar NOT NULL,
  "issue_date" date NOT NULL,
  "complete_date" date NOT NULL,
  "due_date" date NOT NULL,
  "created_at" date NOT NULL,
  "last_updated" date NOT NULL
);

ALTER TABLE "dim_contract" ADD FOREIGN KEY ("personal_data_id") REFERENCES "dim_personal_data" ("personal_data_id");

ALTER TABLE "fact_customers_contracts" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customers" ("customer_id");

ALTER TABLE "fact_customers_contracts" ADD FOREIGN KEY ("contract_id") REFERENCES "dim_contract" ("contract_id");

ALTER TABLE "fact_customers_contracts" ADD FOREIGN KEY ("start_date") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_customers_contracts" ADD FOREIGN KEY ("end_date") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_customers_demographic" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customers" ("customer_id");

ALTER TABLE "fact_customers_demographic" ADD FOREIGN KEY ("location_id") REFERENCES "dim_locations" ("location_id");

ALTER TABLE "fact_customers_demographic" ADD FOREIGN KEY ("date_id") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_customers_usage" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customers" ("customer_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("customer_id") REFERENCES "dim_customers" ("customer_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("contract_id") REFERENCES "dim_contract" ("contract_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("issue_date") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("complete_date") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("due_date") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("created_at") REFERENCES "dim_date" ("date_id");

ALTER TABLE "fact_billing" ADD FOREIGN KEY ("last_updated") REFERENCES "dim_date" ("date_id");

"""


    conn.run(query_create_olap_tables)
    close_db(conn)

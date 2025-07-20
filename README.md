
# fiction_hello
This project is a work in progress and this read me file will be updated overtime.

The project aims to copy some of the behaviours that would be expected in a telecommunication company. The project is devided into 2 components: core and ETL.
### core
The goal from core is to create backend for the project. This includes:
* database design, modeling and normlization. 
* the logic to generate the data.
* AWS EC2 to host the application.
* PistgreSQL hosted on AWS RDS.

### ETL
Aims to create a data pipeline from the previously generateed data to analyse it as well as the new OLAP database to house the data (also hosted on AWS RDS). 


# Getting started
#### 1- To setup your environment locally, run the following commands:

make requirements

make dev-setup

make run-checks

to setup the database:
please navigate to core directory, then run: 
psql -f fiction_hello_db.sql

and make sure to add your .env file to the root directory.

#### 2- to setup your environment on AWS, run the following commands:
make requirements

make dev-setup

make run-checks

navigate to terraform directory
create your terraform .tfvars file inside the terraform directory and add the following variables to it:
db_name     = 
db_user     = 
db_password = 

then run command:
terrform plan
terraform apply -var-file="YourFileName.tfvars"

if successful you will gt 3 outputs:
EC2 IP
EDS Host and port

create your .env file using the port and host you got, make sure to remove the port from the end of the host string you were giving.
ssh into your EC2 instance using the up you got with the following command:
ssh -i /path/to/your/key.pem ec2-user@your-ec2-ip

once in clone the repo
then move the .env file into your EC2 instance using the following command:
scp -i /path/to/your/key.pem /path/to/local/file ec2-user@your-ec2-ip:/the/root/of/you/the-project/on-EC2

run the make file commands again inside the EC2 to make sure everything is sill working.
if successful start your FastAPI server with the following command:
uvicorn main:app --host 0.0.0.0 --port 8000

use your browser to interact with the api, there are to paths currently:
- `healthcheck` which return ok if the server is working .
- `create_records` to generate new Fake customers.



# tech stack
- Python

- Postgresql

- terraform

- AWS (EC2, RDS)

## key dependencies

- `pg8000` – PostgreSQL database driver for Python  
- `python-dotenv` – Loads environment variables from `.env` files  
- `Faker` – Generates realistic fake data for testing and development 
- `FastAPI` – High-performance Python framework for building APIs 


# Auther
Hamoud Alzafiry

[Linkedin](www.linkedin.com/in/hamoud-alzafiry-613135357)

[github](https://github.com/Hamoud9876)

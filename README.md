
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
To set up your environment, run the following Makefile commands:

make requirements

make dev-setup

make run-checks


# tech stack
- Python

- Postgresql

- terraform

- AWS (EC2, RDS)

## key dependencies

- `pg8000` – PostgreSQL database driver for Python  
- `python-dotenv` – Loads environment variables from `.env` files  
- `Faker` – Generates realistic fake data for testing and development 


# Auther
Hamoud Alzafiry

[Linkedin](www.linkedin.com/in/hamoud-alzafiry-613135357)

[github](https://github.com/Hamoud9876)

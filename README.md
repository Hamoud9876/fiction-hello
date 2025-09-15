# 📡 Fiction Hello

A sample project mimicking a telecommunications company’s backend system and ETL / OLAP data pipeline.  
Generates synthetic data, stores it transactionally, transforms and loads into an OLAP database for analytics.

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)  
2. [Architecture](#architecture)  
3. [Tech Stack](#tech-stack)  
4. [Setup & Installation](#setup--installation)  
5. [Docker](#docker)  
6. [Usage](#usage)  
7. [Database Schema](#database-schema)  
8. [Testing](#testing)  
9. [Roadmap](#roadmap)  
10. [Author](#author)  
11. [License](#license)  

---

## 🚀 Project Overview

This project simulates operations of a telecom provider. It provides:

- Backend service for data like customers, contracts, devices, billing, and SIMs.  
- ETL pipeline to ingest, transform, and load into an OLAP schema.  
- Two database layers: transactional + analytical.  

---

## 🏗 Architecture

- **Core**:  
  - API / service layer, data generation (Faker), transactional DB schema.  
- **ETL**:  
  - Ingestion, transformations, OLAP loading.  
- **OLAP DB**:  
  - Dimension and fact tables for analytics.  

---

## ⚙️ Tech Stack

- Python 3.10+  
- FastAPI  
- PostgreSQL  
- SQLAlchemy + pg8000  
- Faker  
- python-dotenv  
- Docker  
- Pytest  

---

## 🛠 Setup & Installation

### Prerequisites

- Python 3.10+  
- PostgreSQL (local or remote)  
- Docker (if using the container)  

### Local Setup (without Docker)

```bash
# Clone repo
git clone https://github.com/Hamoud9876/fiction-hello.git
cd fiction-hello

# Create virtual environment and install dependencies
make requirements

# Create .env file with DB credentials for both OLTP and OLAP:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fiction_hello
DB_USERNAME=...
DB_PASSWORD=...

DB_OLAP_HOST=localhost
DB_OLAP_PORT=5432
DB_OLAP_NAME=fiction_hello
DB_OLAP_USERNAME=...
DB_OLAP_PASSWORD=...


# Run backend locally
uvicorn core.src.api_interface:app --reload

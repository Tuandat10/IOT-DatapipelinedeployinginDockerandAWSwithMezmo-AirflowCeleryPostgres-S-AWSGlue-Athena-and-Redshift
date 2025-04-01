# IOT - Data Pipeline Deploying in Docker and AWS with Mezmo, Airflow, Celery, Postgres, S3, AWS Glue, Athena, and Redshift

## 📌 Introduction
This project provides a comprehensive data pipeline solution to **Extract, Transform, and Load (ETL)** log data from **Mezmo** (where logs from IoT devices are collected) into **Amazon Redshift** for analytics and business insights.

The pipeline leverages a combination of powerful tools and services including **Apache Airflow**, **Celery**, **PostgreSQL**, **Amazon S3**, **AWS Glue**, **Amazon Athena**, and **Amazon Redshift**.

---

## 📚 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [System-Setup](#system-setup)

---

## 🔍 Overview

The pipeline is designed to:

- **Extract** data from **Mezmo** via its API.  
- **Validate and store** raw data and full logs into an **Amazon S3** bucket using Airflow.  
- **Transform** the data using **AWS Glue** and **Amazon Athena**.  
- **Load** the cleaned and structured data into **Amazon Redshift** for analytics and querying.

---

## 🏗️ Architecture

![Architecture Diagram](path/to/your/image.png) <!-- Replace this with the actual path to your architecture image -->

**Components:**
1. **Mezmo API** – Source of the data.
2. **Apache Airflow & Celery** – Orchestrates the ETL process and manages task distribution.
3. **PostgreSQL** – Temporary storage and metadata management.
4. **Amazon S3** – Raw data storage layer.
5. **AWS Glue** – Data cataloging and ETL jobs.
6. **Amazon Athena** – SQL-based transformation engine.
7. **Amazon Redshift** – Data warehousing and analytics.

---

## ✅ Prerequisites

Before getting started, ensure you have the following:

- AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- Mezmo API credentials.
- Docker installed and running.
- Python 3.9 or higher installed.

---

## ⚙️ System Setup

### 1. Clone the Repository

```bash
git clone git@github.com:Tuandat10/IOT-DatapipelinedeployinginDockerandAWSwithMezmo-AirflowCeleryPostgres-S-AWSGlue-Athena-and-Redshift.git
cd IOT-DatapipelinedeployinginDockerandAWSwithMezmo-AirflowCeleryPostgres-S-AWSGlue-Athena-and-Redshift
```
### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Add Your Credentials
```bash
config/config.conf
```
### 5. Start Docker Containers
```bash
docker-compose up -d
```
### 6. Access Airflow UI
```bash
http://localhost:8080
```

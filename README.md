# Olist Data Engineering Pipeline

## Overview

This project is an end-to-end batch Data Engineering pipeline built on the Brazilian Olist e-commerce dataset.

The goal is to transform raw CSV files into clean, analytics-ready tables and business dashboards using a modern data stack: Google Cloud Storage, Apache Spark, BigQuery, dbt, Docker and Looker Studio.

The project simulates a real-world data workflow: ingestion, processing, data warehousing, transformation, modeling and visualization.

## Architecture

![Architecture](docs/architecture.png)

## Tech Stack

* Python
* Apache Spark
* Docker
* Google Cloud Storage
* BigQuery
* dbt
* Looker Studio
* SQL

## Dataset

The project uses the Brazilian Olist E-commerce Public Dataset.

The dataset contains information about orders, customers, products, payments, reviews and geolocation data.

## Pipeline

1. Raw CSV files are stored in Google Cloud Storage.
2. Apache Spark processes and joins the source tables.
3. The processed dataset is written as Parquet.
4. The Parquet data is loaded into BigQuery.
5. dbt builds staging models, fact tables, dimension tables and KPI marts.
6. Looker Studio visualizes the final business metrics.

## Data Modeling

The dbt project follows a layered analytical modeling approach:

* `stg_sales_dataset`
* `fact_sales`
* `dim_customers`
* `dim_products`
* `dim_date`
* `mart_sales_kpis`
* `mart_global_kpis`

## dbt Lineage

![dbt Lineage](docs/dbt_lineage.png)

## Dashboard

The Looker Studio dashboard includes:

* Total revenue
* Number of orders
* Average order value
* Revenue over time
* Revenue by product category
* Revenue by city
* Revenue by state

![Dashboard](docs/dashboard.png)

## Project Structure

```text
olist-data-engineering/
├── data/
│   ├── sample/
│   └── processed/
├── dbt/
├── docs/
│   ├── architecture.png
│   ├── dashboard.png
│   └── dbt_lineage.png
├── src/
│   └── spark_jobs/
├── tests/
├── README.md
└── .gitignore
```

## Future Improvements

* Add Airflow orchestration
* Add CI/CD with GitHub Actions
* Add Docker Compose
* Add Terraform for infrastructure provisioning
* Add product category translation
* Add data quality checks and monitoring

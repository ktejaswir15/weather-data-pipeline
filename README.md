# Weather Data ETL Pipeline - Apache Airflow Orchestration

Daily ETL pipeline that extracts live weather data and loads it into SQLite, orchestrated end-to-end with Apache Airflow.

## What it does

- Airflow DAG with PythonOperators, task dependencies, retry logic, and scheduled daily execution
- Extracts weather data via REST API, transforms with Pandas, loads into SQLite
- Fully containerized with Docker Compose for reproducible, consistent deployment

## Tech stack

Python, Pandas, Apache Airflow, Docker Compose, SQLite, REST API

## How to run

```
docker-compose up
```

Airflow UI will be available at http://localhost:8080. Trigger the DAG manually or let it run on its daily schedule.

## Files

| File | Description |
|---|---|
| dags/weather_dag.py | Main Airflow DAG definition |
| dags/pipeline.py | ETL pipeline logic: extract, transform, load |
| docker-compose.yml | Docker Compose config for Airflow and dependencies |

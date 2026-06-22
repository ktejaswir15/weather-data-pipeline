from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

# Add project path
sys.path.insert(0, 'C:/Users/kteja/OneDrive/Attachments/Desktop/weather-pipeline')

from extract import get_weather, load_to_snowflake

# Cities list
CITIES = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740},
]

default_args = {
    'owner': 'tejaswi',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def extract_and_load():
    """Extract weather data and load to Snowflake"""
    print("Extracting weather data...")
    records = [get_weather(city) for city in CITIES]
    for r in records:
        print(f"  {r['city']}: {r['temperature']}°C")
    print("Loading to Snowflake...")
    load_to_snowflake(records)
    print("✅ Extract and load complete!")

with DAG(
    dag_id='weather_snowflake_dbt_pipeline',
    default_args=default_args,
    description='Daily weather ETL pipeline with Snowflake and dbt',
    schedule_interval='@daily',
    start_date=datetime(2026, 6, 22),
    catchup=False,
    tags=['weather', 'snowflake', 'dbt']
) as dag:

    # Task 1: Extract and load raw data
    extract_load = PythonOperator(
        task_id='extract_and_load_to_snowflake',
        python_callable=extract_and_load
    )

    # Task 2: Run dbt transformations
    dbt_run = BashOperator(
        task_id='run_dbt_transformations',
        bash_command='cd C:/Users/kteja/OneDrive/Attachments/Desktop/weather-pipeline/weather_dbt && dbt run'
    )

    # Task 3: Run dbt tests
    dbt_test = BashOperator(
        task_id='test_dbt_models',
        bash_command='cd C:/Users/kteja/OneDrive/Attachments/Desktop/weather-pipeline/weather_dbt && dbt test'
    )

    # Pipeline order: extract → dbt run → dbt test
    extract_load >> dbt_run >> dbt_test
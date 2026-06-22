# Weather Data Pipeline — Snowflake + dbt + Python

An end-to-end data engineering pipeline that ingests live weather data, loads it into Snowflake, and transforms it using dbt models with automated daily scheduling.

## Architecture
## Tech Stack

- **Python** — Data extraction and Snowflake loading
- **Snowflake** — Cloud data warehouse (RAW schema)
- **dbt** — SQL-based transformation modeling
- **Open-Meteo API** — Free weather data source
- **Python Schedule** — Daily pipeline orchestration

## Pipeline Layers

| Layer | Model | Description |
|---|---|---|
| Raw | WEATHER_RAW | Raw API data loaded via Python |
| Staging | stg_weather | Cleaned data + temp in Fahrenheit + temp category |
| Mart | mart_weather | Final analytics table with comfort index + wind category |

## dbt Models

### stg_weather (Staging)
- Casts and cleans raw weather data
- Adds temperature in Fahrenheit
- Categorizes temperature (Freezing / Cold / Mild / Warm / Hot)

### mart_weather (Mart)
- Computes comfort index (Very Comfortable / Comfortable / Uncomfortable / Very Uncomfortable)
- Classifies wind speed (Calm / Breezy / Windy / Very Windy)
- Final analytics-ready table

## Setup

1. Clone the repo
2. Create `.env` file with Snowflake credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run pipeline: `python scheduler.py`

## Security
- RSA key-pair authentication for Snowflake (no passwords stored)
- Credentials managed via `.env` (excluded from Git)
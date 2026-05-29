# Weather Data Pipeline 

An end-to-end ETL (Extract, Transform, Load) data pipeline built with Python.

## What it does
- **Extracts** live weather data for 5 US cities from a public API
- **Transforms** the data using Pandas (cleaning, sorting, formatting)
- **Loads** the cleaned data into a CSV file
- **Visualizes** temperature by city using Matplotlib

## Technologies Used
- Python
- Pandas
- Matplotlib
- REST API (wttr.in)
- Git & GitHub

## How to Run
pip install requests pandas matplotlib
python pipeline.py

## Output
- weather_data.csv — cleaned weather data table
- weather_chart.png — bar chart of temperatures by city

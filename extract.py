import requests
import snowflake.connector
from datetime import datetime
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
import os

load_dotenv()

# Cities with coordinates
CITIES = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740},
]

def get_weather(city):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={city['lat']}&longitude={city['lon']}"
        f"&current=temperature_2m,relative_humidity_2m,"
        f"apparent_temperature,wind_speed_10m,weather_code"
        f"&temperature_unit=celsius"
    )
    response = requests.get(url)
    data = response.json()
    current = data["current"]

    return {
        "city": city["name"],
        "country": "US",
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "weather_desc": f"weather_code_{current['weather_code']}",
        "wind_speed": current["wind_speed_10m"],
        "extracted_at": datetime.utcnow()
    }

def load_to_snowflake(records):
    with open("snowflake_key.p8", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        private_key=private_key_bytes,
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

    cursor = conn.cursor()
    insert_sql = """
        INSERT INTO WEATHER_RAW 
        (CITY, COUNTRY, TEMPERATURE, FEELS_LIKE, 
         HUMIDITY, WEATHER_DESC, WIND_SPEED, EXTRACTED_AT)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for record in records:
        cursor.execute(insert_sql, (
            record["city"],
            record["country"],
            record["temperature"],
            record["feels_like"],
            record["humidity"],
            record["weather_desc"],
            record["wind_speed"],
            record["extracted_at"]
        ))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Successfully loaded {len(records)} records into Snowflake!")

if __name__ == "__main__":
    print("Extracting weather data...")
    records = [get_weather(city) for city in CITIES]
    for r in records:
        print(f"  {r['city']}: {r['temperature']}°C, humidity: {r['humidity']}%")
    print("Loading to Snowflake...")
    load_to_snowflake(records)
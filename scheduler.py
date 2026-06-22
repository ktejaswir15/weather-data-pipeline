import schedule
import time
import subprocess
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add project path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extract import get_weather, load_to_snowflake

CITIES = [
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Houston", "lat": 29.7604, "lon": -95.3698},
    {"name": "Phoenix", "lat": 33.4484, "lon": -112.0740},
]

DBT_PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather_dbt")

def run_pipeline():
    print("\n" + "="*50)
    print("🚀 Starting Weather Pipeline...")
    print("="*50)
    
    # Step 1: Extract and load
    try:
        print("\n📥 Step 1: Extracting weather data...")
        records = [get_weather(city) for city in CITIES]
        for r in records:
            print(f"  {r['city']}: {r['temperature']}°C, humidity: {r['humidity']}%")
        
        print("\n❄️  Step 2: Loading to Snowflake...")
        load_to_snowflake(records)
        
        # Step 2: Run dbt
        print("\n🔄 Step 3: Running dbt transformations...")
        result = subprocess.run(
            ["dbt", "run"],
            cwd=DBT_PROJECT_DIR,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ dbt error: {result.stderr}")
        else:
            print("✅ dbt transformations complete!")
            
    except Exception as e:
        print(f"❌ Pipeline error: {e}")
    
    print("\n✅ Pipeline complete! Next run in 24 hours.")
    print("="*50)

# Run immediately on start
run_pipeline()

# Then schedule daily at 8 AM
schedule.every().day.at("08:00").do(run_pipeline)

print("\n⏰ Scheduler running — pipeline will run daily at 08:00 AM")
print("Press Ctrl+C to stop\n")

while True:
    schedule.run_pending()
    time.sleep(60)
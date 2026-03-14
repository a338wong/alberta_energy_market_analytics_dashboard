import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE: Download hourly historical weather data for Calgary
# ============================================================

LATITUDE = 51.05
LONGITUDE = -114.07

URL = "https://archive-api.open-meteo.com/v1/archive"

# Historical API should only use past dates
start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": start_date,
    "end_date": end_date,
    "hourly": "temperature_2m,wind_speed_10m",
    "timezone": "America/Edmonton"
}

response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

if "hourly" not in data:
    raise ValueError("Open-Meteo API response missing 'hourly'")

hourly_data = data["hourly"]

df = pd.DataFrame({
    "datetime_he": hourly_data["time"],
    "temperature_c": hourly_data["temperature_2m"],
    "wind_speed_mps": hourly_data["wind_speed_10m"]
})

df["datetime_he"] = pd.to_datetime(df["datetime_he"])

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "weather_data.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

print("Weather data downloaded successfully.")
print(f"Saved to: {OUTPUT_PATH}")
print(f"Date range requested: {start_date} to {end_date}")
print("\nFirst 5 rows:")
print(df.head())
print("\nLast 5 rows:")
print(df.tail())
print("\nRow count:")
print(len(df))

import requests
import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE: Download hourly weather data for Calgary
# ============================================================

LATITUDE = 51.05
LONGITUDE = -114.07

URL = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,wind_speed_10m",
    "timezone": "America/Edmonton"
}

# ============================================================
# CALL THE API
# ============================================================
response = requests.get(URL, params=params, timeout=30)
response.raise_for_status()

# ============================================================
# PARSE JSON RESPONSE
# ============================================================
data = response.json()

if "hourly" not in data:
    raise ValueError("Open-Meteo API response missing 'hourly'")

hourly_data = data["hourly"]

# ============================================================
# LOAD DATA INTO PANDAS DATAFRAME
# ============================================================
df = pd.DataFrame({
    "datetime_he": hourly_data["time"],
    "temperature_c": hourly_data["temperature_2m"],
    "wind_speed_mps": hourly_data["wind_speed_10m"]
})

# ============================================================
# CLEAN DATA TYPES
# ============================================================
df["datetime_he"] = pd.to_datetime(df["datetime_he"])

# ============================================================
# DEFINE OUTPUT PATH
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "weather_data.csv"

# ============================================================
# SAVE DATA
# ============================================================
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

# ============================================================
# PRINT RESULTS
# ============================================================
print("Weather data downloaded successfully.")
print(f"Saved to: {OUTPUT_PATH}")

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nRow count:")
print(len(df))

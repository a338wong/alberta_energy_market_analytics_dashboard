import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE:
# Download hourly weather data for Calgary by combining:
# - Historical archive data (past 365 days through yesterday)
# - Current-day hourly data (today) from forecast endpoint
# ============================================================

LATITUDE = 51.05
LONGITUDE = -114.07
TIMEZONE = "America/Edmonton"

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# ------------------------------------------------------------
# Date windows
# ------------------------------------------------------------
now_local = datetime.now()
today_str = now_local.strftime("%Y-%m-%d")
yesterday_str = (now_local - timedelta(days=1)).strftime("%Y-%m-%d")
start_date_str = (now_local - timedelta(days=365)).strftime("%Y-%m-%d")

# ------------------------------------------------------------
# Helper: build weather dataframe from API payload
# ------------------------------------------------------------
def build_weather_df(hourly_data: dict) -> pd.DataFrame:
    df = pd.DataFrame({
        "datetime_he": hourly_data["time"],
        "temperature_c": hourly_data["temperature_2m"],
        "wind_speed_mps": hourly_data["wind_speed_10m"]
    })
    df["datetime_he"] = pd.to_datetime(df["datetime_he"], errors="coerce")
    df["temperature_c"] = pd.to_numeric(df["temperature_c"], errors="coerce")
    df["wind_speed_mps"] = pd.to_numeric(df["wind_speed_mps"], errors="coerce")
    df = df.dropna(subset=["datetime_he"]).sort_values("datetime_he").reset_index(drop=True)
    return df

# ------------------------------------------------------------
# 1) Historical layer: past 365 days through yesterday
# ------------------------------------------------------------
archive_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": start_date_str,
    "end_date": yesterday_str,
    "hourly": "temperature_2m,wind_speed_10m",
    "timezone": TIMEZONE
}

archive_response = requests.get(ARCHIVE_URL, params=archive_params, timeout=30)
archive_response.raise_for_status()
archive_data = archive_response.json()

if "hourly" not in archive_data:
    raise ValueError("Open-Meteo archive response missing 'hourly'")

archive_df = build_weather_df(archive_data["hourly"])

# ------------------------------------------------------------
# 2) Current-day layer: today from forecast endpoint
# ------------------------------------------------------------
forecast_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "temperature_2m,wind_speed_10m",
    "timezone": TIMEZONE,
    "forecast_days": 1
}

forecast_response = requests.get(FORECAST_URL, params=forecast_params, timeout=30)
forecast_response.raise_for_status()
forecast_data = forecast_response.json()

if "hourly" not in forecast_data:
    raise ValueError("Open-Meteo forecast response missing 'hourly'")

forecast_df = build_weather_df(forecast_data["hourly"])

# Keep only today's rows from the forecast response
forecast_df = forecast_df[forecast_df["datetime_he"].dt.strftime("%Y-%m-%d") == today_str].copy()

# Optional: keep only rows up to the current local hour
current_hour = pd.Timestamp.now(tz=TIMEZONE).floor("h").tz_localize(None)
forecast_df = forecast_df[forecast_df["datetime_he"] <= current_hour].copy()

# ------------------------------------------------------------
# 3) Combine historical + current-day layers
# ------------------------------------------------------------
df = pd.concat([archive_df, forecast_df], ignore_index=True)

# Drop duplicate timestamps, keeping the latest source row
df = df.sort_values("datetime_he").drop_duplicates(subset=["datetime_he"], keep="last")
df = df.reset_index(drop=True)

# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "weather_data.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)

# ------------------------------------------------------------
# Debug output
# ------------------------------------------------------------
print("\n--- WEATHER DEBUG ---")
print("Weather data downloaded successfully.")
print(f"Saved to: {OUTPUT_PATH}")
print(f"Historical date range requested: {start_date_str} to {yesterday_str}")
print(f"Current-day layer requested for: {today_str}")

print("\nRows fetched:")
print(len(df))

print("\nHistorical rows:")
print(len(archive_df))

print("\nCurrent-day rows:")
print(len(forecast_df))

if not df.empty:
    print("\nEarliest weather timestamp:")
    print(df["datetime_he"].min())

    print("\nLatest weather timestamp:")
    print(df["datetime_he"].max())

    print("\nLast 5 weather rows:")
    print(df.tail(5))
else:
    print("Weather dataframe is empty!")

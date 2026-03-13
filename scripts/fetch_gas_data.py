import os
import requests
import pandas as pd
from pathlib import Path

API_KEY =  os.environ["FRED_API_KEY"]

# DO NOT EXPOSE THIS KEY
# FRED endpoint for time series observations
URL = "https://api.stlouisfed.org/fred/series/observations"

# Series ID for Henry Hub Natural Gas Spot Price
SERIES_ID = "DHHNGSP"

# Build an output path that works relative to this script's location
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "gas_price.csv"


# ============================================================
# DEFINE API PARAMETERS
# ============================================================
# These parameters are sent to the FRED API.
# series_id = which dataset we want
# api_key   = your personal FRED key
# file_type = return JSON so Python can read it easily
params = {
    "series_id": SERIES_ID,
    "api_key": API_KEY,
    "file_type": "json"
}

# ============================================================
# CALL THE API
# ============================================================
# requests.get() sends an HTTP GET request to the FRED API.
# timeout=30 prevents the script from hanging forever if something goes wrong.
response = requests.get(URL, params=params, timeout=30)

# Raise an error if the request failed (for example, bad API key)
response.raise_for_status()

# ============================================================
# PARSE JSON RESPONSE
# ============================================================
# Convert the API response into a Python dictionary
data = response.json()

if "observations" not in data:
    raise ValueError("FRED API response missing 'observations'")

# ============================================================
# LOAD INTO A PANDAS DATAFRAME
# ============================================================
# This turns the list of observations into a table structure
df = pd.DataFrame(data["observations"])

# ============================================================
# KEEP ONLY THE COLUMNS WE NEED
# ============================================================
# FRED returns extra metadata columns like:
# - realtime_start
# - realtime_end
# We only need:
# - date
# - value
df = df[["date", "value"]]

# ============================================================
# RENAME COLUMNS
# ============================================================
# Rename "value" to something more meaningful for the project
df.columns = ["date", "gas_price"]

# ============================================================
# CLEAN DATA TYPES
# ============================================================
# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Convert gas_price to numeric
# errors="coerce" means invalid values become NaN instead of crashing
df["gas_price"] = pd.to_numeric(df["gas_price"], errors="coerce")

# ============================================================
# OPTIONAL DATA CLEANING
# ============================================================
# Remove rows where gas_price is missing
df = df.dropna(subset=["gas_price"])

# Sort by date ascending, just to keep everything neat
df = df.sort_values("date").reset_index(drop=True)


# ============================================================
# SAVE TO CSV
# ============================================================
# Save the cleaned data for Power BI
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_PATH, index=False)


# ============================================================
# PRINT RESULTS FOR A QUICK CHECK
# ============================================================
print("Gas price data downloaded successfully.")
print(f"Saved to: {OUTPUT_PATH}")
print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nRow count:")
print(len(df))

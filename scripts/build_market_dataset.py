import pandas as pd
from pathlib import Path

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE:
# Build the final analytics dataset by combining:
# - AESO pool price data (hourly)
# - Natural gas prices (daily)
# - Weather data (hourly)
#
# OUTPUT:
# market_dataset.csv → processed dataset
# market_data_export.csv → fixed file for Power BI refresh
# ============================================================


# ============================================================
# DEFINE PROJECT FILE PATHS
# ============================================================
# Resolve the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Define locations of input datasets
POOL_PATH = BASE_DIR.parent / "data" / "processed" / "pool_price.csv"
GAS_PATH = BASE_DIR.parent / "data" / "raw" / "gas_price.csv"
WEATHER_PATH = BASE_DIR.parent / "data" / "raw" / "weather_data.csv"

# Define output file locations
OUTPUT_PATH = BASE_DIR.parent / "data" / "processed" / "market_dataset.csv"
EXPORT_PATH = BASE_DIR.parent / "data" / "processed" / "market_data_export.csv"

# Ensure output folder exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# VERIFY REQUIRED INPUT FILES EXIST
# ============================================================
# If any required dataset is missing, stop execution early.
required_files = [POOL_PATH, GAS_PATH, WEATHER_PATH]
missing_files = [str(path) for path in required_files if not path.exists()]

if missing_files:
    raise FileNotFoundError(f"Missing required input files: {missing_files}")


# ============================================================
# LOAD DATASETS
# ============================================================
# Read CSV files into pandas DataFrames
pool = pd.read_csv(POOL_PATH)
gas = pd.read_csv(GAS_PATH)
weather = pd.read_csv(WEATHER_PATH)


# ============================================================
# STANDARDIZE DATETIME COLUMNS
# ============================================================
# Convert string timestamps into pandas datetime objects
# "errors='coerce'" converts invalid timestamps into NaT
# which we remove in the next step.

pool["datetime_he"] = pd.to_datetime(pool["datetime_he"], errors="coerce").dt.floor("h")
gas["date"] = pd.to_datetime(gas["date"], errors="coerce")
weather["datetime_he"] = pd.to_datetime(weather["datetime_he"], errors="coerce").dt.floor("h")


# ============================================================
# REMOVE INVALID TIMESTAMPS
# ============================================================
# Drop rows where datetime conversion failed
pool = pool.dropna(subset=["datetime_he"])
gas = gas.dropna(subset=["date"])
weather = weather.dropna(subset=["datetime_he"])


# ============================================================
# OPTIONAL: ADJUST WEATHER TIMESTAMP (IF NEEDED)
# ============================================================
# Some electricity datasets use "Hour Ending" timestamps
# while weather APIs use "Hour Beginning".
#
# If your pool price data represents Hour Ending values,
# you may need to shift weather data forward by one hour.
#
# Uncomment this line if timestamps appear misaligned:
#
# weather["datetime_he"] = weather["datetime_he"] + pd.Timedelta(hours=1)


# ============================================================
# CREATE DAILY DATE COLUMN FOR GAS MERGE
# ============================================================
# Pool price data is hourly while gas price data is daily.
# We create a daily column so each hourly observation
# can inherit the latest available gas price.

pool["date"] = pool["datetime_he"].dt.floor("D")


# ============================================================
# SORT DATASETS BEFORE MERGING
# ============================================================
# merge_asof requires sorted inputs
pool = pool.sort_values("date").reset_index(drop=True)
gas = gas.sort_values("date").reset_index(drop=True)


# ============================================================
# MERGE GAS PRICES INTO HOURLY POOL DATA
# ============================================================
# Gas price is daily while pool price is hourly.
#
# merge_asof with direction="backward" assigns the most
# recent gas price available for each hourly observation.

df = pd.merge_asof(
    pool,
    gas,
    on="date",
    direction="backward"
)


# ============================================================
# DEBUG: CHECK DATETIME RANGES BEFORE WEATHER MERGE
# ============================================================
# This helps diagnose merge problems if weather columns
# appear as NaN in the final dataset.

print("\nPOOL datetime range:")
print(df["datetime_he"].min(), "to", df["datetime_he"].max())

print("\nWEATHER datetime range:")
print(weather["datetime_he"].min(), "to", weather["datetime_he"].max())


# ============================================================
# MERGE WEATHER DATA
# ============================================================
# Weather data is hourly, so we perform a direct join
# on the hourly timestamp.

df = df.sort_values("datetime_he").reset_index(drop=True)
weather = weather.sort_values("datetime_he").reset_index(drop=True)

df = df.merge(
    weather,
    on="datetime_he",
    how="left"
)


# ============================================================
# DEBUG: CHECK FOR MISSING WEATHER VALUES
# ============================================================
print("\nNull counts after weather merge:")
print(df[["temperature_c", "wind_speed_mps"]].isna().sum())


# ============================================================
# CALCULATE SPARK SPREAD
# ============================================================
# Spark Spread estimates profitability of gas-fired power plants.
#
# Formula:
# Spark Spread = Power Price – (Gas Price × Heat Rate)
#
# Heat Rate represents the amount of gas required to generate
# one MWh of electricity. Typical Alberta combined-cycle
# heat rate ≈ 7–8 mmBtu/MWh.

HEAT_RATE = 7.5

df["spark_spread"] = df["pool_price"] - (df["gas_price"] * HEAT_RATE)

# --------------------------------------------------
# Feature engineering
# --------------------------------------------------
# Heating Degree Days (HDD)
# Proxy for cold-weather power demand pressure.
# Base temperature = 18°C
df["hdd"] = (18 - df["temperature_c"]).clip(lower=0)

# 24-hour rolling average demand
# Smooths hourly noise and shows short-term demand trend
df["demand_24h_avg"] = df["demand_mw"].rolling(window=24, min_periods=1).mean()


# ============================================================
# SELECT FINAL COLUMNS FOR DASHBOARD
# ============================================================
df = df[
    [
        "datetime_he",
        "pool_price",
        "demand_mw",
        "demand_24h_avg",
        "gas_price",
        "temperature_c",
        "wind_speed_mps",
        "hdd",
        "spark_spread",
    ]
]


# ============================================================
# SORT DATASET
# ============================================================
# Ensure dataset is ordered chronologically
df = df.sort_values("datetime_he").reset_index(drop=True)


# ============================================================
# SAVE OUTPUT DATASETS
# ============================================================
# market_dataset.csv → general processed dataset
# market_data_export.csv → fixed filename for Power BI refresh

df.to_csv(OUTPUT_PATH, index=False)
df.to_csv(EXPORT_PATH, index=False)


# ============================================================
# PRINT SUMMARY
# ============================================================
print("\nMarket dataset created.")
print("Saved to:", OUTPUT_PATH)
print("Exported dataset for Power BI:", EXPORT_PATH)

print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nData types:")
print(df.dtypes)

print("\nRow count:")
print(len(df))

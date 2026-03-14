import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

POOL_PATH = BASE_DIR.parent / "data" / "processed" / "pool_price.csv"
GAS_PATH = BASE_DIR.parent / "data" / "raw" / "gas_price.csv"
WEATHER_PATH = BASE_DIR.parent / "data" / "raw" / "weather_data.csv"

OUTPUT_PATH = BASE_DIR.parent / "data" / "processed" / "market_dataset.csv"
EXPORT_PATH = BASE_DIR.parent / "data" / "processed" / "market_data_export.csv"

# Make sure output folder exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Check required input files
# --------------------------------------------------
required_files = [POOL_PATH, GAS_PATH, WEATHER_PATH]
missing_files = [str(path) for path in required_files if not path.exists()]

if missing_files:
    raise FileNotFoundError(f"Missing required input files: {missing_files}")

# --------------------------------------------------
# Load datasets
# --------------------------------------------------
pool = pd.read_csv(POOL_PATH)
gas = pd.read_csv(GAS_PATH)
weather = pd.read_csv(WEATHER_PATH)

# --------------------------------------------------
# Convert datetime columns
# --------------------------------------------------
pool["datetime_he"] = pd.to_datetime(pool["datetime_he"], errors="coerce")
gas["date"] = pd.to_datetime(gas["date"], errors="coerce")
weather["datetime_he"] = pd.to_datetime(weather["datetime_he"], errors="coerce")

# Drop bad rows before merging
pool = pool.dropna(subset=["datetime_he"])
gas = gas.dropna(subset=["date"])
weather = weather.dropna(subset=["datetime_he"])

# Create daily date column in pool data
pool["date"] = pool["datetime_he"].dt.floor("D")

# Sort before merge_asof
pool = pool.sort_values("date").reset_index(drop=True)
gas = gas.sort_values("date").reset_index(drop=True)

# --------------------------------------------------
# Merge using nearest previous gas date
# --------------------------------------------------
# Gas data is daily and pool data is hourly.
# merge_asof with direction="backward" uses the latest
# available prior gas price for each hourly pool price row.
df = pd.merge_asof(
    pool,
    gas,
    on="date",
    direction="backward"
)

# --------------------------------------------------
# Merge weather 
# --------------------------------------------------
weather = weather.sort_values("datetime_he").reset_index(drop=True)
df = df.sort_values("datetime_he").reset_index(drop=True)

df = pd.merge_asof(
    df,
    weather,
    on="datetime_he",
    direction="nearest",
    tolerance=pd.Timedelta("1H")
)

# --------------------------------------------------
# Spark Spread Calculation
# --------------------------------------------------
# Spark Spread = Power Price – (Gas Price * Heat Rate)
HEAT_RATE = 7.5

df["spark_spread"] = df["pool_price"] - (df["gas_price"] * HEAT_RATE)

# --------------------------------------------------
# Final column selection
# --------------------------------------------------
df = df[
    [
        "datetime_he",
        "pool_price",
        "demand_mw",
        "gas_price",
        "temperature_c",
        "wind_speed_mps",
        "spark_spread",
    ]
]

# Sort by hourly timestamp
df = df.sort_values("datetime_he").reset_index(drop=True)

# --------------------------------------------------
# Save outputs
# --------------------------------------------------
# market_dataset.csv = general processed dataset
# market_data_export.csv = fixed file for Power BI / OneDrive sync
df.to_csv(OUTPUT_PATH, index=False)
df.to_csv(EXPORT_PATH, index=False)

# --------------------------------------------------
# Print summary
# --------------------------------------------------
print("Market dataset created.")
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

import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_raw.csv"
OUTPUT_PATH = BASE_DIR.parent / "data" / "processed" / "pool_price.csv"

# Make sure the output folder exists
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Load raw AESO file
# --------------------------------------------------
# Your file has extra rows above the real header:
# Row 1: "Pool Price"
# Row 2: blank
# Row 3: actual header row
df = pd.read_csv(INPUT_PATH, skiprows=4)

print("Original columns:")
print(df.columns)

expected_cols = ["Date (HE)", "Price ($)", "AIL Demand (MW)"]
missing_cols = [col for col in expected_cols if col not in df.columns]

if missing_cols:
    raise ValueError(f"Missing expected columns in AESO file: {missing_cols}")

# --------------------------------------------------
# Keep only the columns we need
# --------------------------------------------------
df = df[["Date (HE)", "Price ($)", "AIL Demand (MW)"]].copy()

# --------------------------------------------------
# Rename columns to cleaner names
# --------------------------------------------------
df.columns = ["datetime_he", "pool_price", "demand_mw"]

# --------------------------------------------------
# Clean values
# --------------------------------------------------
# Convert Date (HE) into datetime
df["datetime_he"] = pd.to_datetime(df["datetime_he"], errors="coerce")

# Convert numeric columns
# The AESO file may contain "-" for unavailable values
df["pool_price"] = pd.to_numeric(df["pool_price"], errors="coerce")
df["demand_mw"] = pd.to_numeric(df["demand_mw"], errors="coerce")

# --------------------------------------------------
# Remove bad rows
# --------------------------------------------------
df = df.dropna(subset=["datetime_he", "pool_price"])

# --------------------------------------------------
# Sort chronologically
# --------------------------------------------------
df = df.sort_values("datetime_he").reset_index(drop=True)

# --------------------------------------------------
# Save cleaned file
# --------------------------------------------------
df.to_csv(OUTPUT_PATH, index=False)

# --------------------------------------------------
# Debug output
# --------------------------------------------------
print("\n--- POOL PRICE DEBUG ---")

print("Saved cleaned pool price data to:")
print(OUTPUT_PATH)

print("\nRows after cleaning:")
print(len(df))

if not df.empty:
    print("\nEarliest pool datetime:")
    print(df["datetime_he"].min())

    print("\nLatest pool datetime:")
    print(df["datetime_he"].max())

    print("\nLast 3 pool rows:")
    print(df.tail(3))

    print("\nData types:")
    print(df.dtypes)
else:
    print("Pool price dataframe is empty!")

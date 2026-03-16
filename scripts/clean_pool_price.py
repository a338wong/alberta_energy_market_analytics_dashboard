import pandas as pd
from pathlib import Path

# --------------------------------------------------
# File paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
HISTORICAL_INPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_raw.csv"
CURRENT_INPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_current_raw.csv"
OUTPUT_PATH = BASE_DIR.parent / "data" / "processed" / "pool_price.csv"

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Helper to parse AESO pool CSV
# --------------------------------------------------
def load_pool_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")

    df = pd.read_csv(path, skiprows=4)

    print(f"\n--- {label.upper()} ORIGINAL COLUMNS ---")
    print(df.columns)

    expected_cols = ["Date (HE)", "Price ($)", "AIL Demand (MW)"]
    missing_cols = [col for col in expected_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"{label} missing expected columns: {missing_cols}")

    df = df[["Date (HE)", "Price ($)", "AIL Demand (MW)"]].copy()
    df.columns = ["datetime_he", "pool_price", "demand_mw"]

    df["datetime_he"] = pd.to_datetime(df["datetime_he"], errors="coerce")
    df["pool_price"] = pd.to_numeric(df["pool_price"], errors="coerce")
    df["demand_mw"] = pd.to_numeric(df["demand_mw"], errors="coerce")

    print(f"\n--- {label.upper()} PRE-DROP DEBUG ---")
    print("Rows before dropping nulls:")
    print(len(df))

    print("\nLast 10 parsed rows before dropna:")
    print(df.tail(10))

    df = df.dropna(subset=["datetime_he", "pool_price"])
    df = df.sort_values("datetime_he").reset_index(drop=True)

    print(f"\n--- {label.upper()} POST-DROP DEBUG ---")
    print("Rows after dropping nulls:")
    print(len(df))

    if not df.empty:
        print("\nEarliest datetime:")
        print(df["datetime_he"].min())

        print("\nLatest datetime:")
        print(df["datetime_he"].max())

        print("\nLast 5 rows:")
        print(df.tail(5))
    else:
        print(f"{label} dataframe is empty after cleaning.")

    return df

# --------------------------------------------------
# Load both historical and current layers
# --------------------------------------------------
historical_df = load_pool_csv(HISTORICAL_INPUT_PATH, "historical")
current_df = load_pool_csv(CURRENT_INPUT_PATH, "current")

# --------------------------------------------------
# Combine layers
# --------------------------------------------------
combined = pd.concat([historical_df, current_df], ignore_index=True)

# Keep latest copy when timestamps overlap
combined = combined.sort_values("datetime_he").drop_duplicates(
    subset=["datetime_he"], keep="last"
).reset_index(drop=True)

# --------------------------------------------------
# Save cleaned file
# --------------------------------------------------
combined.to_csv(OUTPUT_PATH, index=False)

# --------------------------------------------------
# Final debug output
# --------------------------------------------------
print("\n--- FINAL POOL PRICE DEBUG ---")
print("Saved cleaned combined pool price data to:")
print(OUTPUT_PATH)

print("\nRows after combining:")
print(len(combined))

if not combined.empty:
    print("\nEarliest pool datetime:")
    print(combined["datetime_he"].min())

    print("\nLatest pool datetime:")
    print(combined["datetime_he"].max())

    print("\nLast 10 pool rows:")
    print(combined.tail(10))

    print("\nData types:")
    print(combined.dtypes)
else:
    print("Combined pool price dataframe is empty!")

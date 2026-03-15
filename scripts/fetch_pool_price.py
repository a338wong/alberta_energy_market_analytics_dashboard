import requests
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE: Download raw AESO historical pool price CSV
# WINDOW: Last 90 days
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_raw.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Build rolling 90-day date window
# AESO historical endpoint expects MMDDYYYY
# --------------------------------------------------
today = datetime.now()
start_date = (today - timedelta(days=90)).strftime("%m%d%Y")
end_date = today.strftime("%m%d%Y")

# --------------------------------------------------
# AESO historical pool price report endpoint
# --------------------------------------------------
URL = (
    "http://ets.aeso.ca/ets_web/ip/Market/Reports/"
    f"HistoricalPoolPriceReportServlet?beginDate={start_date}"
    f"&endDate={end_date}&contentType=csv"
)

# --------------------------------------------------
# Download file
# --------------------------------------------------
response = requests.get(URL, timeout=60)
response.raise_for_status()

with open(OUTPUT_PATH, "wb") as f:
    f.write(response.content)

# --------------------------------------------------
# Debug output
# --------------------------------------------------
print("\n--- RAW POOL FILE DEBUG ---")
print("Downloaded raw historical pool price file successfully.")
print("Saved to:", OUTPUT_PATH)
print("File size (bytes):", OUTPUT_PATH.stat().st_size)
print("Date range requested:", start_date, "to", end_date)
print("Request URL:", URL)

with open(OUTPUT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    preview = []
    for _ in range(5):
        line = f.readline()
        if not line:
            break
        preview.append(line.rstrip("\n"))

print("\nFirst 5 raw lines:")
for line in preview:
    print(line)

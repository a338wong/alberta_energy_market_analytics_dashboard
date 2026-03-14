import requests
from pathlib import Path

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE: Download raw AESO current pool price CSV
# ============================================================

URL = "http://ets.aeso.ca/ets_web/ip/Market/Reports/SMPriceReportServlet?beginDate=&endDate=&contentType=csv"

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_raw.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

response = requests.get(URL, timeout=60)
response.raise_for_status()

with open(OUTPUT_PATH, "wb") as f:
    f.write(response.content)

print("\n--- RAW POOL FILE DEBUG ---")
print("Downloaded raw pool price file successfully.")
print("Saved to:", OUTPUT_PATH)
print("File size (bytes):", OUTPUT_PATH.stat().st_size)

with open(OUTPUT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    preview = [next(f).rstrip("\n") for _ in range(5)]

print("\nFirst 5 raw lines:")
for line in preview:
    print(line)

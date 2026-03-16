import requests
from pathlib import Path

# ============================================================
# PROJECT: Alberta Energy Market Analytics Dashboard
# PURPOSE: Download current AESO pool price CSV
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_PATH = BASE_DIR.parent / "data" / "raw" / "pool_price_current_raw.csv"
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

URL = (
    "http://ets.aeso.ca/ets_web/ip/Market/Reports/"
    "SMPriceReportServlet?beginDate=&endDate=&contentType=csv"
)

response = requests.get(URL, timeout=60)
response.raise_for_status()

with open(OUTPUT_PATH, "wb") as f:
    f.write(response.content)

print("\n--- CURRENT POOL RAW DEBUG ---")
print("Downloaded current pool price file successfully.")
print("Saved to:", OUTPUT_PATH)
print("File size (bytes):", OUTPUT_PATH.stat().st_size)
print("Request URL:", URL)

with open(OUTPUT_PATH, "r", encoding="utf-8", errors="ignore") as f:
    preview = []
    for _ in range(8):
        line = f.readline()
        if not line:
            break
        preview.append(line.rstrip("\n"))

print("\nFirst 8 raw lines:")
for line in preview:
    print(line)

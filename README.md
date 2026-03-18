# Alberta Energy Market Analytics Dashboard ⚡

## Table of Contents 📚
1. [Project Description](#project-description)
2. [Live Dashboard](#live-dashboard)
3. [How to Run the Project](#how-to-run-the-project)
4. [How to Use the Project](#how-to-use-the-project)
5. [Data Pipeline & Methodology](#data-pipeline--methodology)
6. [Tech Stack](#tech-stack)
7. [Demo](#demo)
8. [Future Improvements](#future-improvements)
9. [Credits](#credits)

---

## Project Description 📋

This project is an end-to-end energy market analytics dashboard that tracks and visualizes key drivers of Alberta’s electricity market, including power prices, demand, natural gas prices, and weather conditions.

The system automates data collection, transformation, and reporting to simulate a real-world analytics workflow used in energy trading, market analysis, and risk management.

---

## Live Dashboard 🌐

*Interactive dashboard available upon request*

---

## Dashboard Preview 📊
![Dashboard](assets/dashboard.png)

---

## How to Run the Project 🛠️

To run the data pipeline locally:

### 1. Clone the Repository
```bash
git clone https://github.com/a338wong/alberta_energy_market_analytics_dashboard.git
cd alberta_energy_market_analytics_dashboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Data Pipeline
```bash
python scripts/fetch_gas_data.py
python scripts/fetch_weather_data.py
python scripts/clean_pool_price.py
python scripts/build_market_dataset.py
```

### 4. Open Dashboard
- Open the Power BI file (`.pbix`)
- Refresh data to view updated metrics

---

## How to Use the Project 📖

1. View KPI cards for:
   - Pool price ($/MWh)
   - Electricity demand (MW)
   - Natural gas prices
   - Spark spread

2. Analyze time-series charts to:
   - Identify price trends
   - Compare demand vs price behavior
   - Observe weather impact on energy markets

3. Use the dashboard to understand:
   - Market dynamics
   - Cost drivers of electricity
   - Relationships between gas and power pricing

---

## Data Pipeline & Methodology 📈

### 1. Data Collection
- **AESO** → Alberta pool price & demand  
- **FRED API** → Natural gas prices  
- **Weather API** → Temperature & wind speed  

---

### 2. Data Processing
- Raw datasets are cleaned and standardized
- Time-series data is aligned across sources
- Missing values and inconsistencies are handled
- Final dataset is merged into a unified structure

---

### 3. Feature Engineering
- Spark spread calculation (power vs gas economics)
- Time-based features (daily trends, rolling windows)
- KPI aggregation for dashboard metrics

---

### 4. Automation
- GitHub Actions runs the pipeline on a scheduled basis
- Data is refreshed automatically
- Updated dataset is stored in the repository

---

### 5. Visualization
- Power BI dashboard displays:
  - KPI cards
  - Time-series trends
  - Comparative analysis across variables

---

## Tech Stack 💻

- Python (Pandas, Requests)  
- GitHub Actions (automation / CI-CD)  
- Power BI (data visualization)  
- APIs (AESO, FRED, Weather)  
- CSV-based data pipeline  

---

## Demo 🎥

*Dashboard demo available upon request*

---

## Future Improvements 🚀

- Real-time data streaming integration  
- Forecasting models for price and demand  
- Alert system for price spikes  
- Database integration (Snowflake / BigQuery)  
- Enhanced financial metrics and volatility analysis  

---

## Credits 🏆

- **Alan Wong**  
  - GitHub: https://github.com/a338wong  
  - LinkedIn: https://www.linkedin.com/in/alan-wong-309160212/  

---

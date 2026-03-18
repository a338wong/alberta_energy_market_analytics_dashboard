# Alberta Energy Market Analytics Dashboard ⚡

## Table of Contents 📚
1. [Project Description](#project-description)
2. [Project Objective](#project-objective)
3. [Key Questions the Dashboard Answers](#key-questions-the-dashboard-answers)
4. [Live Dashboard](#live-dashboard)
5. [How to Run the Project](#how-to-run-the-project)
6. [How to Use the Project](#how-to-use-the-project)
7. [Data Pipeline & Methodology](#data-pipeline--methodology)
8. [Tech Stack](#tech-stack)
9. [Limitations](#limitations)
10. [Future Improvements](#future-improvements)
11. [Credits](#credits)

---

## Project Description 📋

This project is an end-to-end energy market analytics dashboard that tracks and visualizes key drivers of Alberta’s electricity market, including power prices, demand, natural gas prices, and weather conditions.

The system automates data collection, transformation, and reporting to simulate a real-world analytics workflow used in energy trading, market analysis, and risk management.

---

## Project Objective 🎯

Build an interactive Power BI dashboard analyzing Alberta energy market dynamics, focusing on how electricity prices respond to changes in:

- Electricity demand  
- Natural gas prices  
- Weather conditions  

The dashboard enables users to explore relationships between these variables to better understand **energy price volatility and market conditions in Alberta**.

---

## Key Questions the Dashboard Answers ❓

### 1️⃣ What drives electricity price volatility in Alberta?
- Analyze price spikes and volatility patterns  
- Examine price distributions over time  

---

### 2️⃣ When does electricity demand peak?
- Identify hourly demand trends  
- Compare weekday vs weekend demand  
- Analyze seasonal demand patterns  

---

### 3️⃣ How does weather influence energy demand?
- Compare temperature vs electricity demand  
- Evaluate seasonal weather effects  

---

### 4️⃣ How are natural gas prices related to electricity prices?
- Analyze correlation between gas and power prices  
- Track gas price trends alongside electricity price movements  
- Understand spark spread dynamics  

---

## Live Dashboard 🌐

*Interactive dashboard available upon request*

---

## Dashboard Preview 📊
![Dashboard](assets/dashboard.png)

---

## How to Run the Project 🛠️

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
- Open the Power BI `.pbix` file  
- Refresh data to view updated metrics  

---

## How to Use the Project 📖

1. Monitor KPI cards for:
   - Pool price ($/MWh)  
   - Electricity demand (MW)  
   - Natural gas prices  
   - Spark spread  

2. Analyze time-series charts to:
   - Identify price trends and volatility  
   - Compare demand vs price behavior  
   - Observe weather impact on energy consumption  

3. Use the dashboard to:
   - Understand market dynamics  
   - Evaluate cost drivers of electricity  
   - Explore relationships between gas and power markets  

---

## Data Pipeline & Methodology 📈

### 1. Data Collection
- AESO → Alberta pool price & demand  
- FRED API → Natural gas prices  
- Weather API → Temperature & wind speed  

---

### 2. Data Processing
- Clean and standardize raw datasets  
- Align time-series data across sources  
- Handle missing values and inconsistencies  
- Merge into a unified dataset  

---

### 3. Feature Engineering
- Spark spread calculation  
- Time-based aggregations  
- KPI metric construction  

---

### 4. Automation
- GitHub Actions schedules pipeline execution  
- Data is refreshed automatically  
- Processed dataset is stored in the repository  

---

### 5. Visualization
- Power BI dashboard includes:
  - KPI cards  
  - Time-series charts  
  - Comparative analytics  

---

## Tech Stack 💻

- Python (Pandas, Requests)  
- GitHub Actions (CI/CD automation)  
- Power BI (data visualization)  
- APIs (AESO, FRED, Weather)  
- CSV-based data pipeline  

---

## Limitations ⚠️

- **FRED API latency**: Natural gas price data is not always updated daily, which can introduce lag in analysis  
- **GitHub Actions scheduling delays**: Workflow execution may not run exactly on schedule due to queueing or runtime delays  
- **Power BI refresh limits**: Free-tier accounts have restrictions on refresh frequency, limiting near real-time updates  
- **Data granularity differences**: Some datasets (e.g., gas vs electricity) may have different update frequencies and resolutions  
- **Public data constraints**: Data availability and quality depend on external APIs  

---

## Future Improvements 🚀

- **Alternative data sources for natural gas** to reduce reliance on FRED API latency (e.g., more frequently updated market data providers)
- **Forecasting models** for electricity prices and demand (e.g., time-series or machine learning approaches)  
- **Grid congestion & constraint analysis** to identify transmission bottlenecks and their impact on price spikes       
- **Advanced analytics** including volatility modeling, correlation analysis, and scenario testing  
- **Alerting system** for significant market events (e.g., price spikes, demand surges)  

---

## Credits 🏆

- **Alan Wong**  
  - GitHub: https://github.com/a338wong  
  - LinkedIn: https://www.linkedin.com/in/alan-wong-309160212/  

---

# Alberta Energy Market Analytics Dashboard

## Table of Contents
1. [Project Description](#project-description)
2. [Project Objective](#project-objective)
3. [Key Questions the Dashboard Answers](#key-questions-the-dashboard-answers)
4. [Live Dashboard](#live-dashboard)
5. [Data Pipeline and Methodology](#data-pipeline-and-methodology)
6. [Tech Stack](#tech-stack)
7. [Limitations](#limitations)
8. [Future Improvements](#future-improvements)
9. [Credits](#credits)

## Project Description

This project is an end-to-end energy market analytics dashboard that tracks and visualizes key drivers of Alberta’s electricity market, including power prices, demand, natural gas prices, and weather conditions.

The system automates data collection, transformation, and reporting to simulate a real-world analytics workflow used in energy trading, market analysis, and risk management.

## Project Objective

Build an interactive Power BI dashboard analyzing Alberta energy market dynamics, focusing on how electricity prices respond to changes in:

- Electricity demand  
- Natural gas prices  
- Weather conditions  

The dashboard enables users to explore relationships between these variables to better understand energy price volatility and market conditions in Alberta.

## Key Questions the Dashboard Answers

### 1. What drives electricity price volatility in Alberta?
- Analyze price spikes and volatility patterns  
- Examine price distributions over time  

### 2. When does electricity demand peak?
- Identify hourly demand trends  
- Compare weekday vs weekend demand  
- Analyze seasonal demand patterns  

### 3. How does weather influence energy demand?
- Compare temperature vs electricity demand  
- Evaluate seasonal weather effects  

### 4. How are natural gas prices related to electricity prices?
- Analyze the correlation between gas and power prices  
- Track gas price trends alongside electricity price movements  
- Understand spark spread dynamics  

## Live Dashboard

Interactive dashboard available upon request

## Dashboard Preview
![Dashboard](assets/dashboard.png)

## Data Pipeline and Methodology

### 1. Data Collection
- AESO → Alberta pool price and demand  
- FRED API → Natural gas prices  
- Weather API → Temperature and wind speed  

### 2. Data Processing
- Clean, align, and merge datasets into a unified time-series dataset  

### 3. Feature Engineering
- Spark spread calculation  
- Time-based aggregations  
- KPI metric construction  

### 4. Automation
- GitHub Actions schedules pipeline execution  
- Processed dataset is updated automatically  

### 5. Visualization
- Power BI dashboard with KPI cards and time-series analysis  

## Tech Stack

- Python (Pandas, Requests)  
- GitHub Actions (CI/CD automation)  
- Power BI (data visualization)  
- APIs (AESO, FRED, Weather)  
- CSV-based data pipeline  

## Limitations

- FRED API latency: Natural gas data is not always updated daily  
- GitHub Actions delays: Scheduled jobs may not run exactly on time  
- Power BI refresh limits: Free-tier restricts refresh frequency  
- Data granularity differences across sources  
- Dependence on external APIs for data availability  

## Future Improvements

- Alternative data sources for natural gas to reduce reliance on FRED API  
- Forecasting models for electricity prices and demand  
- Grid congestion and constraint analysis for price spike drivers  
- Advanced analytics including volatility modeling and correlation analysis  
- Alerting system for significant market events  

## Credits

- Alan Wong  
  - GitHub: https://github.com/a338wong  
  - LinkedIn: https://www.linkedin.com/in/a338wong/  

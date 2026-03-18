# Alberta Energy Market Analytics Dashboard

An end-to-end data pipeline and visualization dashboard analyzing key drivers of Alberta’s electricity market, including power prices, demand, natural gas prices, and weather conditions.

## Dashboard Preview

![Dashboard Preview](assets/dashboard_preview.png)

## Download Dashboard

[Download Power BI File (.pbix)](https://github.com/a338wong/alberta_energy_market_analytics_dashboard/raw/main/reports/Alberta_Energy_Dashboard.pbix)

*The dashboard is provided as a `.pbix` file for full functionality in Power BI Desktop (Windows only).  
It can also be uploaded to Power BI Service (web) using a work or school account, though data refresh may require additional configuration.*

## Project Overview

This project tracks and analyzes how electricity prices respond to changes in key market drivers:

- Electricity demand  
- Natural gas prices  
- Weather conditions  

The system automates data collection, transformation, and reporting to simulate a real-world analytics workflow used in energy trading, market analysis, and risk management.

The dashboard enables users to explore relationships between these variables to better understand energy price volatility and market conditions in Alberta.

## Key Questions the Dashboard Answers

### What drives electricity price volatility in Alberta?
- Analyze price spikes and volatility patterns  
- Examine price distributions over time  

### When does electricity demand peak?
- Identify hourly demand trends  
- Compare weekday vs weekend demand  
- Analyze seasonal demand patterns  

### How does weather influence energy demand?
- Compare temperature vs electricity demand  
- Evaluate seasonal weather effects  

### How are natural gas prices related to electricity prices?
- Analyze the correlation between gas and power prices  
- Track gas price trends alongside electricity price movements  
- Understand spark spread dynamics  

## Data Pipeline and Methodology

### Data Collection
- AESO → Alberta pool price and demand  
- FRED API → Natural gas prices  
- Weather API → Temperature and wind speed  

### Data Processing
- Clean, align, and merge datasets into a unified time-series dataset  

### Feature Engineering
- Spark spread calculation  
- Time-based aggregations  
- KPI metric construction  

### Automation
- GitHub Actions schedules pipeline execution  
- Processed dataset is updated automatically  

### Visualization
- Power BI dashboard with KPI cards and time-series analysis  

## Tech Stack

- Python (Pandas, Requests)  
- GitHub Actions (CI/CD automation)  
- Power BI (data visualization)  
- APIs (AESO, FRED, Weather)  
- CSV-based data pipeline  

## Limitations

- Natural gas data from FRED is not always updated daily  
- GitHub Actions scheduling may introduce slight delays  
- Differences in data granularity across sources  
- Dependence on external APIs for data availability  

Power BI Deployment Constraint:  
- Due to restrictions associated with Power BI free-tier and school-managed accounts, the dashboard cannot be published publicly via Power BI Service.  
- To address this, the full `.pbix` file is provided above for local interaction and exploration.

## Future Improvements

- Alternative data sources for natural gas to reduce reliance on FRED API  
- Forecasting models for electricity prices and demand  
- Grid congestion and constraint analysis for price spike drivers  
- Advanced analytics, including volatility modeling and correlation analysis  
- Alerting system for significant market events  

## Credits

- Alan Wong  
  - GitHub: https://github.com/a338wong  
  - LinkedIn: https://www.linkedin.com/in/a338wong/  

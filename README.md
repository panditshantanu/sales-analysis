# Sales Data Analysis Dashboard 📊

A comprehensive pandas practice project for analyzing e-commerce sales data and building insights.

## Project Overview
This project focuses on analyzing sales data from an online retail company to uncover business insights, trends, and patterns using pandas data analysis techniques.

## Learning Objectives
- **Data Cleaning**: Handle missing values, duplicates, and data type conversions
- **Exploratory Data Analysis**: Statistical summaries and data profiling
- **Time Series Analysis**: Sales trends over time, seasonality patterns
- **Groupby Operations**: Sales by region, product, customer segments
- **Data Visualization**: Charts and plots using matplotlib/seaborn
- **Business Insights**: Revenue analysis, top performers, growth metrics

## Dataset Features
- **Orders**: Order ID, customer info, dates, shipping details
- **Products**: Product categories, prices, costs, suppliers
- **Customers**: Demographics, location, customer lifetime value
- **Sales**: Revenue, quantity, discounts, profit margins

## Project Structure
```
├── data/
│   ├── raw/                 # Original datasets
│   ├── processed/           # Cleaned datasets
│   └── sample_data_generator.py
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_sales_analysis.ipynb
│   ├── 04_customer_analysis.ipynb
│   └── 05_dashboard_creation.ipynb
├── src/
│   ├── data_processing.py
│   ├── analysis_functions.py
│   └── visualization_helpers.py
└── requirements.txt
```

## Getting Started
1. Install required packages: `pip install -r requirements.txt`
2. Generate sample data: `python data/sample_data_generator.py`
3. Start with `notebooks/01_data_exploration.ipynb`

## Skill Progression
- **Beginner**: Data loading, basic filtering, simple aggregations
- **Intermediate**: Complex groupby, pivot tables, time series analysis
- **Advanced**: Multi-table joins, advanced visualizations, business metrics

Happy analyzing! 🚀

"""
Data Processing Helper Functions for Sales Analysis
Contains reusable functions for data cleaning and preprocessing.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def load_sales_data(data_path='../data/raw/'):
    """
    Load all sales datasets and return as a dictionary.
    
    Parameters:
    data_path (str): Path to the raw data folder
    
    Returns:
    dict: Dictionary containing all dataframes
    """
    try:
        datasets = {}
        datasets['customers'] = pd.read_csv(f'{data_path}customers.csv')
        datasets['products'] = pd.read_csv(f'{data_path}products.csv')
        datasets['orders'] = pd.read_csv(f'{data_path}orders.csv')
        datasets['sales'] = pd.read_csv(f'{data_path}sales.csv')
        
        print(f"✅ Loaded {len(datasets)} datasets successfully")
        return datasets
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def clean_sales_data(datasets):
    """
    Clean and preprocess the sales datasets.
    
    Parameters:
    datasets (dict): Dictionary containing raw dataframes
    
    Returns:
    dict: Dictionary containing cleaned dataframes
    """
    customers_df = datasets['customers'].copy()
    products_df = datasets['products'].copy()
    orders_df = datasets['orders'].copy()
    sales_df = datasets['sales'].copy()
    
    # Convert date columns
    customers_df['registration_date'] = pd.to_datetime(customers_df['registration_date'])
    products_df['launch_date'] = pd.to_datetime(products_df['launch_date'])
    orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
    orders_df['shipped_date'] = pd.to_datetime(orders_df['shipped_date'])
    orders_df['delivered_date'] = pd.to_datetime(orders_df['delivered_date'])
    
    return {
        'customers': customers_df,
        'products': products_df,
        'orders': orders_df,
        'sales': sales_df
    }

def create_comprehensive_dataset(datasets):
    """
    Create a comprehensive dataset by merging all tables.
    
    Parameters:
    datasets (dict): Dictionary containing cleaned dataframes
    
    Returns:
    pd.DataFrame: Comprehensive sales analysis dataset
    """
    sales_df = datasets['sales']
    orders_df = datasets['orders']
    products_df = datasets['products']
    customers_df = datasets['customers']
    
    # Merge all datasets
    comprehensive_df = sales_df.merge(orders_df, on='order_id', how='left') \
                              .merge(products_df, on='product_id', how='left') \
                              .merge(customers_df, on='customer_id', how='left')
    
    # Add derived columns
    comprehensive_df['profit_margin'] = (comprehensive_df['profit'] / comprehensive_df['total_amount']) * 100
    comprehensive_df['year'] = comprehensive_df['order_date'].dt.year
    comprehensive_df['month'] = comprehensive_df['order_date'].dt.month
    comprehensive_df['quarter'] = comprehensive_df['order_date'].dt.quarter
    comprehensive_df['day_of_week'] = comprehensive_df['order_date'].dt.day_name()
    comprehensive_df['month_name'] = comprehensive_df['order_date'].dt.month_name()
    comprehensive_df['delivery_days'] = (comprehensive_df['delivered_date'] - comprehensive_df['order_date']).dt.days
    
    return comprehensive_df

def calculate_business_metrics(df):
    """
    Calculate key business metrics from the sales data.
    
    Parameters:
    df (pd.DataFrame): Comprehensive sales dataset
    
    Returns:
    dict: Dictionary containing business metrics
    """
    metrics = {
        'total_revenue': df['total_amount'].sum(),
        'total_profit': df['profit'].sum(),
        'total_orders': df['order_id'].nunique(),
        'total_customers': df['customer_id'].nunique(),
        'total_products_sold': df['quantity'].sum(),
        'avg_order_value': df.groupby('order_id')['total_amount'].sum().mean(),
        'avg_profit_margin': df['profit_margin'].mean(),
        'date_range': (df['order_date'].min(), df['order_date'].max())
    }
    
    return metrics

def get_top_performers(df, metric='total_amount', group_by='product_id', top_n=10):
    """
    Get top performers by any metric and grouping.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    metric (str): Metric to rank by
    group_by (str): Column to group by
    top_n (int): Number of top performers to return
    
    Returns:
    pd.DataFrame: Top performers
    """
    if group_by == 'product_id':
        result = df.groupby(['product_id', 'product_name']).agg({
            'total_amount': 'sum',
            'profit': 'sum',
            'quantity': 'sum'
        }).sort_values(metric, ascending=False).head(top_n)
    else:
        result = df.groupby(group_by)[metric].sum().sort_values(ascending=False).head(top_n)
    
    return result

def analyze_trends(df, time_period='month'):
    """
    Analyze sales trends over time.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    time_period (str): Time period for analysis ('day', 'week', 'month', 'quarter')
    
    Returns:
    pd.DataFrame: Trend analysis results
    """
    if time_period == 'month':
        trends = df.groupby(df['order_date'].dt.to_period('M')).agg({
            'total_amount': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'quantity': 'sum'
        })
    elif time_period == 'quarter':
        trends = df.groupby(['year', 'quarter']).agg({
            'total_amount': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'quantity': 'sum'
        })
    elif time_period == 'day_of_week':
        trends = df.groupby('day_of_week').agg({
            'total_amount': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'quantity': 'sum'
        })
    
    return trends

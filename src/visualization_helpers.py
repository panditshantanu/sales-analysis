"""
Visualization Helper Functions for Sales Analysis
Contains reusable plotting functions for consistent visualizations.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def setup_plotting_style():
    """Setup consistent plotting style for matplotlib and seaborn."""
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10

def plot_sales_dashboard(df, figsize=(16, 12)):
    """
    Create a comprehensive sales dashboard with multiple visualizations.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    figsize (tuple): Figure size for the dashboard
    
    Returns:
    matplotlib.figure.Figure: Dashboard figure
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle('📊 Sales Performance Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Monthly Revenue Trend
    monthly_revenue = df.groupby(df['order_date'].dt.to_period('M'))['total_amount'].sum()
    monthly_revenue.plot(kind='line', ax=axes[0,0], marker='o', linewidth=2)
    axes[0,0].set_title('📈 Monthly Revenue Trend')
    axes[0,0].set_ylabel('Revenue ($)')
    axes[0,0].grid(True, alpha=0.3)
    
    # 2. Category Performance
    category_sales = df.groupby('category')['total_amount'].sum().sort_values(ascending=True)
    category_sales.plot(kind='barh', ax=axes[0,1], color='skyblue')
    axes[0,1].set_title('🏷️ Revenue by Category')
    axes[0,1].set_xlabel('Revenue ($)')
    
    # 3. Customer Segment Analysis
    segment_sales = df.groupby('customer_segment')['total_amount'].sum()
    axes[0,2].pie(segment_sales.values, labels=segment_sales.index, autopct='%1.1f%%', startangle=90)
    axes[0,2].set_title('👥 Revenue by Customer Segment')
    
    # 4. Daily Sales Pattern
    daily_pattern = df.groupby('day_of_week')['total_amount'].sum().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ])
    daily_pattern.plot(kind='bar', ax=axes[1,0], color='lightcoral')
    axes[1,0].set_title('📅 Sales by Day of Week')
    axes[1,0].set_ylabel('Revenue ($)')
    axes[1,0].tick_params(axis='x', rotation=45)
    
    # 5. Profit Margin by Category
    profit_margin = df.groupby('category')['profit_margin'].mean().sort_values(ascending=True)
    profit_margin.plot(kind='barh', ax=axes[1,1], color='lightgreen')
    axes[1,1].set_title('💰 Avg Profit Margin by Category')
    axes[1,1].set_xlabel('Profit Margin (%)')
    
    # 6. Quarterly Performance
    quarterly_sales = df.groupby(['year', 'quarter'])['total_amount'].sum()
    quarterly_sales.plot(kind='bar', ax=axes[1,2], color='orange')
    axes[1,2].set_title('📊 Quarterly Sales')
    axes[1,2].set_ylabel('Revenue ($)')
    axes[1,2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    return fig

def plot_time_series_interactive(df, metric='total_amount', title='Sales Trend'):
    """
    Create an interactive time series plot using Plotly.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    metric (str): Metric to plot
    title (str): Chart title
    
    Returns:
    plotly.graph_objects.Figure: Interactive plot
    """
    monthly_data = df.groupby(df['order_date'].dt.to_period('M')).agg({
        'total_amount': 'sum',
        'profit': 'sum',
        'order_id': 'nunique',
        'quantity': 'sum'
    }).reset_index()
    
    monthly_data['order_date'] = monthly_data['order_date'].astype(str)
    
    fig = px.line(monthly_data, x='order_date', y=metric, 
                  title=title, markers=True,
                  hover_data=['total_amount', 'profit', 'order_id'])
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title=metric.replace('_', ' ').title(),
        hovermode='x unified'
    )
    
    return fig

def plot_top_products(df, top_n=10, metric='total_amount'):
    """
    Create a horizontal bar chart of top products.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    top_n (int): Number of top products to show
    metric (str): Metric to rank by
    
    Returns:
    plotly.graph_objects.Figure: Bar chart
    """
    top_products = df.groupby(['product_id', 'product_name']).agg({
        'total_amount': 'sum',
        'profit': 'sum',
        'quantity': 'sum'
    }).sort_values(metric, ascending=False).head(top_n)
    
    fig = px.bar(top_products.reset_index(), 
                 x=metric, y='product_name',
                 orientation='h',
                 title=f'Top {top_n} Products by {metric.replace("_", " ").title()}',
                 hover_data=['total_amount', 'profit', 'quantity'])
    
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def plot_heatmap(df, x_col, y_col, value_col):
    """
    Create a heatmap for analyzing relationships between categorical variables.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    x_col (str): Column for x-axis
    y_col (str): Column for y-axis
    value_col (str): Column for values (aggregated)
    
    Returns:
    matplotlib.figure.Figure: Heatmap figure
    """
    pivot_data = df.groupby([x_col, y_col])[value_col].sum().unstack(fill_value=0)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(pivot_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax)
    ax.set_title(f'{value_col.replace("_", " ").title()} by {x_col} and {y_col}')
    plt.tight_layout()
    
    return fig

def plot_distribution(df, column, bins=30):
    """
    Plot distribution of a numerical column.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    column (str): Column to plot
    bins (int): Number of bins for histogram
    
    Returns:
    matplotlib.figure.Figure: Distribution plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Histogram
    df[column].hist(bins=bins, ax=axes[0], edgecolor='black', alpha=0.7)
    axes[0].set_title(f'Distribution of {column.replace("_", " ").title()}')
    axes[0].set_xlabel(column.replace("_", " ").title())
    axes[0].set_ylabel('Frequency')
    
    # Box plot
    df.boxplot(column=column, ax=axes[1])
    axes[1].set_title(f'Box Plot of {column.replace("_", " ").title()}')
    axes[1].set_ylabel(column.replace("_", " ").title())
    
    plt.tight_layout()
    return fig

def create_summary_table(df, group_by, metrics=['total_amount', 'profit', 'quantity']):
    """
    Create a summary table with key metrics by a grouping variable.
    
    Parameters:
    df (pd.DataFrame): Sales dataset
    group_by (str): Column to group by
    metrics (list): List of metrics to calculate
    
    Returns:
    pd.DataFrame: Summary table
    """
    summary = df.groupby(group_by)[metrics].agg(['sum', 'mean', 'count']).round(2)
    summary.columns = [f'{metric}_{stat}' for metric, stat in summary.columns]
    return summary.sort_values(f'{metrics[0]}_sum', ascending=False)

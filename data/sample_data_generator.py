"""
Sales Data Generator for Pandas Practice
Creates realistic e-commerce sales data for analysis practice.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Initialize Faker for generating realistic data
fake = Faker()
np.random.seed(42)  # For reproducible results
random.seed(42)

def generate_customers(n_customers=1000):
    """Generate customer data"""
    print(f"Generating {n_customers} customers...")
    
    customers = []
    for i in range(n_customers):
        customer = {
            'customer_id': f'CUST_{i+1:05d}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'city': fake.city(),
            'state': fake.state(),
            'country': fake.country(),
            'postal_code': fake.postcode(),
            'registration_date': fake.date_between(start_date='-3y', end_date='today'),
            'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], p=[0.2, 0.5, 0.3]),
            'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], p=[0.15, 0.25, 0.25, 0.2, 0.15])
        }
        customers.append(customer)
    
    return pd.DataFrame(customers)

def generate_products(n_products=500):
    """Generate product catalog"""
    print(f"Generating {n_products} products...")
    
    categories = [
        'Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports & Outdoors',
        'Health & Beauty', 'Toys & Games', 'Automotive', 'Food & Beverages', 'Office Supplies'
    ]
    
    subcategories = {
        'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Audio', 'Gaming'],
        'Clothing': ['Men\'s Clothing', 'Women\'s Clothing', 'Shoes', 'Accessories'],
        'Home & Garden': ['Furniture', 'Kitchen', 'Bedroom', 'Garden Tools'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children\'s Books'],
        'Sports & Outdoors': ['Fitness', 'Outdoor Gear', 'Team Sports', 'Water Sports']
    }
    
    products = []
    for i in range(n_products):
        category = np.random.choice(categories)
        subcategory = np.random.choice(subcategories.get(category, [category]))
        
        # Price based on category
        if category == 'Electronics':
            base_price = np.random.uniform(50, 2000)
        elif category == 'Clothing':
            base_price = np.random.uniform(20, 300)
        elif category == 'Books':
            base_price = np.random.uniform(10, 50)
        else:
            base_price = np.random.uniform(15, 500)
        
        cost = base_price * np.random.uniform(0.4, 0.7)  # Cost is 40-70% of price
        
        product = {
            'product_id': f'PROD_{i+1:05d}',
            'product_name': fake.catch_phrase(),
            'category': category,
            'subcategory': subcategory,
            'price': round(base_price, 2),
            'cost': round(cost, 2),
            'supplier': fake.company(),
            'launch_date': fake.date_between(start_date='-2y', end_date='today'),
            'weight_kg': round(np.random.uniform(0.1, 10), 2),
            'rating': round(np.random.uniform(3.0, 5.0), 1)
        }
        products.append(product)
    
    return pd.DataFrame(products)

def generate_orders_and_sales(customers_df, products_df, n_orders=5000):
    """Generate orders and sales data"""
    print(f"Generating {n_orders} orders with sales data...")
    
    orders = []
    sales = []
    
    # Date range for orders (last 2 years)
    start_date = datetime.now() - timedelta(days=730)
    end_date = datetime.now()
    
    for i in range(n_orders):
        # Generate order
        order_date = fake.date_between_dates(start_date, end_date)
        customer_id = np.random.choice(customers_df['customer_id'])
        
        # Shipping info
        shipping_days = int(np.random.choice([1, 2, 3, 5, 7], p=[0.1, 0.3, 0.3, 0.2, 0.1]))
        shipped_date = order_date + timedelta(days=shipping_days)
        delivered_date = shipped_date + timedelta(days=int(np.random.randint(1, 8)))
        
        order = {
            'order_id': f'ORD_{i+1:06d}',
            'customer_id': customer_id,
            'order_date': order_date,
            'shipped_date': shipped_date,
            'delivered_date': delivered_date,
            'shipping_method': np.random.choice(['Standard', 'Express', 'Overnight'], p=[0.6, 0.3, 0.1]),
            'shipping_cost': round(np.random.uniform(5, 25), 2),
            'order_status': np.random.choice(['Completed', 'Cancelled', 'Returned'], p=[0.85, 0.1, 0.05])
        }
        orders.append(order)
        
        # Generate 1-5 items per order
        n_items = int(np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05]))
        
        for j in range(n_items):
            product = products_df.sample(1).iloc[0]
            quantity = int(np.random.choice([1, 2, 3, 4], p=[0.7, 0.2, 0.07, 0.03]))
            
            # Apply discount sometimes
            discount_rate = 0
            if np.random.random() < 0.3:  # 30% chance of discount
                discount_rate = float(np.random.choice([0.05, 0.10, 0.15, 0.20, 0.25], p=[0.4, 0.3, 0.15, 0.1, 0.05]))
            
            unit_price = product['price']
            discount_amount = unit_price * discount_rate
            final_price = unit_price - discount_amount
            
            sale = {
                'sale_id': f'SALE_{i+1:06d}_{j+1}',
                'order_id': order['order_id'],
                'product_id': product['product_id'],
                'quantity': quantity,
                'unit_price': unit_price,
                'discount_rate': discount_rate,
                'discount_amount': round(discount_amount, 2),
                'final_price': round(final_price, 2),
                'total_amount': round(final_price * quantity, 2),
                'cost_per_unit': product['cost'],
                'total_cost': round(product['cost'] * quantity, 2),
                'profit': round((final_price - product['cost']) * quantity, 2)
            }
            sales.append(sale)
    
    return pd.DataFrame(orders), pd.DataFrame(sales)

def save_data(customers_df, products_df, orders_df, sales_df):
    """Save all datasets to CSV files"""
    print("Saving datasets...")
    
    # Create output directory
    output_dir = os.path.join('data', 'raw')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save datasets
    customers_df.to_csv(os.path.join(output_dir, 'customers.csv'), index=False)
    products_df.to_csv(os.path.join(output_dir, 'products.csv'), index=False)
    orders_df.to_csv(os.path.join(output_dir, 'orders.csv'), index=False)
    sales_df.to_csv(os.path.join(output_dir, 'sales.csv'), index=False)
    
    print(f"✅ Data saved to {output_dir}/")
    
    # Print summary statistics
    print("\n📊 Dataset Summary:")
    print(f"Customers: {len(customers_df):,} records")
    print(f"Products: {len(products_df):,} records")
    print(f"Orders: {len(orders_df):,} records")
    print(f"Sales: {len(sales_df):,} records")
    print(f"Total Revenue: ${sales_df['total_amount'].sum():,.2f}")
    print(f"Total Profit: ${sales_df['profit'].sum():,.2f}")
    print(f"Date Range: {orders_df['order_date'].min()} to {orders_df['order_date'].max()}")

def main():
    """Generate all sample data"""
    print("🚀 Generating Sales Data for Pandas Practice...")
    print("=" * 50)
    
    # Generate datasets
    customers_df = generate_customers(1000)
    products_df = generate_products(500)
    orders_df, sales_df = generate_orders_and_sales(customers_df, products_df, 5000)
    
    # Save to files
    save_data(customers_df, products_df, orders_df, sales_df)
    
    print("\n✨ Data generation complete!")
    print("📁 Check the 'data/raw/' folder for your datasets")
    print("📓 Start with '01_data_exploration.ipynb' to begin your analysis!")

if __name__ == "__main__":
    main()

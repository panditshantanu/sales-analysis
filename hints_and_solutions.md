# 💡 Hints & Solutions - Use Only When Stuck!

## 🎯 Learning Tips:
- **Try first, then peek** - Always attempt the exercise before looking here
- **Don't copy-paste** - Type the code yourself to build muscle memory
- **Experiment** - Modify the solutions to see what happens

---

## Exercise 1.1 Hints:
```python
# Column names
print(df.columns)

# Shape
print(f"Shape: {df.shape}")

# Data types  
print(df.dtypes)

# Missing values
print(df.isnull().sum())
```

## Exercise 1.2 Hints:
```python
# Basic filtering
df[df['quantity'] > 3]
df[df['category'] == 'Electronics']
df[df['customer'] == 'Alice']

# Combining conditions (use & and parentheses)
df[(df['customer'] == 'Alice') & (df['category'] == 'Electronics') & (df['quantity'] > 2)]
```

## Exercise 2.1 Hints:
```python
# Basic groupby operations
df.groupby('customer')['total_amount'].sum()
df.groupby('category')['price'].mean()
df['product'].value_counts()
df.groupby('customer')['total_amount'].max()
```

## Exercise 2.2 Hints:
```python
# Multiple aggregations
df.groupby('customer').agg({
    'total_amount': 'sum',
    'quantity': 'mean', 
    'date': 'count'  # Count of orders
})

# Pivot table
pd.pivot_table(df, 
               values='total_amount', 
               index='customer', 
               columns='category', 
               aggfunc='sum',
               fill_value=0)
```

## Exercise 3.1 Hints:
```python
# Bar chart
customer_sales = df.groupby('customer')['total_amount'].sum()
customer_sales.plot(kind='bar', title='Sales by Customer')

# Line plot over time
daily_sales = df.groupby('date')['total_amount'].sum()
daily_sales.plot(kind='line', title='Sales Over Time')

# Histogram
df['total_amount'].plot(kind='hist', bins=20, title='Distribution of Sales')
```

## Exercise 4 Hints:
```python
# Best customer
best_customer = df.groupby('customer')['total_amount'].sum().sort_values(ascending=False)
print(f"Best customer: {best_customer.index[0]} with ${best_customer.iloc[0]:.2f}")

# Discount analysis
discounted = df[df['discount'] > 0]['total_amount'].mean()
no_discount = df[df['discount'] == 0]['total_amount'].mean()
print(f"Average sale with discount: ${discounted:.2f}")
print(f"Average sale without discount: ${no_discount:.2f}")
```

---

## 🔧 Common Pandas Patterns:

### Data Exploration
```python
df.head()           # First 5 rows
df.tail()           # Last 5 rows  
df.info()           # Data types and memory
df.describe()       # Statistical summary
df.shape            # (rows, columns)
df.columns          # Column names
```

### Filtering
```python
df[df['column'] > value]                    # Single condition
df[(df['col1'] > val1) & (df['col2'] < val2)]  # Multiple conditions
df[df['column'].isin(['val1', 'val2'])]     # Multiple values
```

### Groupby
```python
df.groupby('column').sum()                  # Single aggregation
df.groupby('column').agg(['sum', 'mean'])   # Multiple aggregations
df.groupby(['col1', 'col2']).sum()          # Multiple grouping columns
```

### Visualization
```python
df['column'].plot(kind='hist')              # Histogram
df.groupby('cat')['val'].sum().plot(kind='bar')  # Bar chart
df.plot(x='date', y='value', kind='line')   # Line plot
```

---

**Remember**: The goal is to learn, not to get the "right" answer quickly. Take your time and experiment!

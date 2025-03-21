import numpy as np
import pandas as pd
import random
import string

# np.random.seed(42)

# weeks = pd.date_range(start='2024-01-07', periods=52, freq='W')
# product_id = list(range(1,51))
# a = list(string.ascii_lowercase + string.ascii_uppercase)
# product_name = []
# for i in range(50):
#     product_name.append(''.join(random.choices(a, k=3)))
# print(product_name)
# units_sold = np.random.randint(1, 100, size=(52, 50))
# print(units_sold)

# price_per_unit = np.random.rand(50) * 120.324

# repeated_values = np.repeat(weeks,50)
# df = pd.DataFrame(repeated_values, columns=['week'])
# df['product_id'] = product_id * 52
# df['product_name'] = np.tile(product_name, 52)
# df['units_sold'] = units_sold.flatten()
# df['price_per_unit'] = np.tile(price_per_unit, 52)
# df['total_sales'] = df['units_sold'] * df['price_per_unit']
# df['total_sales'] = df['total_sales'].round(2)
# df['total_sales'] = df['total_sales'].astype(float)
# df['price_per_unit'] = df['price_per_unit'].round(2)
# df['price_per_unit'] = df['price_per_unit'].astype(float)
# df['units_sold'] = df['units_sold'].astype(int)
# df['region'] = np.tile('USA',2600)


def generate_sales_data():
    """
    Generates a DataFrame with sales data for 50 products over 52 weeks.
    Each row represents the sales data for a specific product in a specific week.
    The DataFrame contains the following columns:
    - week: The week of the year (date).
    - product_id: The ID of the product.
    - product_name: The name of the product.
    - units_sold: The number of units sold.
    - price_per_unit: The price per unit of the product.
    - total_sales: The total sales amount (units_sold * price_per_unit).
    - region: The region where the sales occurred (default is 'USA').
    """
    np.random.seed(42)
    weeks = pd.date_range(start='2024-01-07', periods=52, freq='W')
    product_id = list(range(1, 51))
    a = list(string.ascii_lowercase + string.ascii_uppercase)
    product_name = []
    for i in range(50):
        product_name.append(''.join(random.choices(a, k=3)))
    units_sold = np.random.randint(1, 100, size=(52, 50))
    price_per_unit = np.random.rand(50) * 120.324
    repeated_values = np.repeat(weeks, 50)
    df = pd.DataFrame(repeated_values, columns=['week'])
    df['product_id'] = product_id * 52
    df['product_name'] = np.tile(product_name, 52)
    df['units_sold'] = units_sold.flatten()
    df['price_per_unit'] = np.tile(price_per_unit, 52)
    df['total_sales'] = df['units_sold'] * df['price_per_unit']
    df['total_sales'] = df['total_sales'].round(2)
    df['total_sales'] = df['total_sales'].astype(float)
    df['price_per_unit'] = df['price_per_unit'].round(2)
    df['price_per_unit'] = df['price_per_unit'].astype(float)
    df['units_sold'] = df['units_sold'].astype(int)
    df['region'] = np.tile('USA', 2600)
    df['date'] = df['week']
    return df

if __name__ == "__main__":
    sales_data = generate_sales_data()
    sales_data.to_csv('data/sales_data.csv', index=False)
    print("Sales data generated and saved to 'sales_data.csv'.")
    print(sales_data.head())
    
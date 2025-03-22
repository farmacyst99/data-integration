from dotenv import load_dotenv
import os
import gas_api
import cpi_api
import generate_data
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Defining variables for series_id, api_key, observation_start, and observation_end
series_id_gas = "GASREGW"
series_id_cpi = "CPIAUCNS"
observation_start = "2023-12-31"
observation_end = "2024-12-24"
api_key = os.getenv("FRED_API")
# Check if the API key is loaded
if api_key is None:
    raise ValueError("API key not found. Please set the FRED_API environment variable.")



# Fetching gas prices and CPI data
# from FRED API

sales_df = generate_data.generate_sales_data()
gas_df = gas_api.fetch_gas_prices(series_id=series_id_gas, api_key=api_key, observation_start=observation_start, observation_end=observation_end)
cpi_df = cpi_api.fetch_consumer_price_index(series_id=series_id_cpi, api_key=api_key, observation_start=observation_start, observation_end=observation_end)


# Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
cpi_df['date'] = pd.to_datetime(cpi_df['date'])
#cpi_df.set_index(cpi_df['date'], inplace=True)
cpi_df['month'] = cpi_df['date'].dt.to_period('M')

#sales_df['date'] = pd.to_datetime(sales_df['date'])
sales_df['month'] = sales_df['date'].dt.to_period('M')

#print(sales_df)
#print(cpi_df)

# Merge sales_df and cpi_df on month
merged_df = pd.merge(sales_df, cpi_df, on='month', how='inner')
merged_df = merged_df.drop(columns=['month','date_y'])
merged_df.rename(columns={'date_x': 'date','value':'cpi_value'}, inplace=True)

# Now we have to obtain week number and create a new column for merged_df and gas_df
gas_df['date'] = pd.to_datetime(gas_df['date'])
gas_df['week_num'] = gas_df['date'].dt.isocalendar().week
merged_df['week_num'] = merged_df['date'].dt.isocalendar().week
# Merge gas_df and merged_df on week_num
final_df = pd.merge(merged_df, gas_df, on='week_num', how='inner')
final_df = final_df.drop(columns=['week_num','date_y'])
final_df.rename(columns={'date_x': 'week_start_date','value':'gas_value'}, inplace=True)
final_df.to_csv('data/final_data.csv', index=False)
print(final_df)



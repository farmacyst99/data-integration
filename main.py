import gas_api
import cpi_api
import generate_data
import pandas as pd



sales_data = generate_data.generate_sales_data()
gas_data = gas_api.fetch_gas_prices("bd7ee64d6749a1bd68c358548a4a8c81", "GASREGW", "2024-01-07", "2024-12-24")
cpi_data = cpi_api.fetch_consumer_price_index("CPIAUCNS", "bd7ee64d6749a1bd68c358548a4a8c81", "2024-01-07", "2024-12-24")
print(cpi_data['date'])
print(gas_data['date'])
print(sales_data['date'])

# Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
cpi_data['date'] = pd.to_datetime(cpi_data['date'])
cpi_data.set_index(cpi_data['date'], inplace=True)
cpi_data['date'] = cpi_data['date'].dt.to_period('M')
expanded_cpi_data = cpi_data.set_index('date').resample('6D').ffill().reset_index()

expanded_cpi_data['date'] = expanded_cpi_data['date'].dt.start_time

print(expanded_cpi_data)



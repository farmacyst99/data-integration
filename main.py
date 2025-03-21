#!/usr/bin/python
import gas_api
import cpi_api 
import generate_data 


sales_data = generate_data.generate_sales_data()
gas_data = gas_api.fetch_gas_prices("bd7ee64d6749a1bd68c358548a4a8c81", "GASREGW", "2024-01-07", "2024-12-24")
cpi_data = cpi_api.fetch_consumer_price_index("CPIAUCNS", "bd7ee64d6749a1bd68c358548a4a8c81", "2024-01-07", "2024-12-24")

# Merge the data


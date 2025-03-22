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


# # Check if the API key is loaded
# if api_key is None:
#     raise ValueError("API key not found. Please set the FRED_API environment variable.")



# # Fetching gas prices and CPI data
# # from FRED API

# sales_df = generate_data.generate_sales_data()
# gas_df = gas_api.fetch_gas_prices(series_id=series_id_gas, api_key=api_key, observation_start=observation_start, observation_end=observation_end)
# cpi_df = cpi_api.fetch_consumer_price_index(series_id=series_id_cpi, api_key=api_key, observation_start=observation_start, observation_end=observation_end)


# # Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
# cpi_df['date'] = pd.to_datetime(cpi_df['date'])
# #cpi_df.set_index(cpi_df['date'], inplace=True)
# cpi_df['month'] = cpi_df['date'].dt.to_period('M')

# #sales_df['date'] = pd.to_datetime(sales_df['date'])
# sales_df['month'] = sales_df['date'].dt.to_period('M')

# #print(sales_df)
# #print(cpi_df)

# # Merge sales_df and cpi_df on month
# merged_df = pd.merge(sales_df, cpi_df, on='month', how='inner')
# merged_df = merged_df.drop(columns=['month','date_y'])
# merged_df.rename(columns={'date_x': 'date','value':'cpi_value'}, inplace=True)

# # Now we have to obtain week number and create a new column for merged_df and gas_df
# gas_df['date'] = pd.to_datetime(gas_df['date'])
# gas_df['week_num'] = gas_df['date'].dt.isocalendar().week
# merged_df['week_num'] = merged_df['date'].dt.isocalendar().week
# # Merge gas_df and merged_df on week_num
# final_df = pd.merge(merged_df, gas_df, on='week_num', how='inner')
# final_df = final_df.drop(columns=['week_num','date_y'])
# final_df.rename(columns={'date_x': 'week_start_date','value':'gas_value'}, inplace=True)
# final_df.to_csv('data/final_data.csv', index=False)
# print(final_df)


# Convert the above process into a function
def fetch_and_merge_data(series_id_gas, series_id_cpi, observation_start, observation_end, api_key):
    # Fetching gas prices and CPI data
    sales_df = generate_data.generate_sales_data()
    gas_df = gas_api.fetch_gas_prices(series_id=series_id_gas, api_key=api_key, observation_start=observation_start, observation_end=observation_end)
    cpi_df = cpi_api.fetch_consumer_price_index(series_id=series_id_cpi, api_key=api_key, observation_start=observation_start, observation_end=observation_end)

    # Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
    cpi_df['date'] = pd.to_datetime(cpi_df['date'])
    cpi_df['month'] = cpi_df['date'].dt.to_period('M')

    # Conevert sales_df['date'] to datetime format
    #sales_df['date'] = pd.to_datetime(sales_df['date'])
    sales_df['month'] = sales_df['date'].dt.to_period('M')

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
    
    return final_df


def validate_data(final_df):
    '''
    Validate the final DataFrame to ensure it meets the required criteria.
    Stores all errors into a separate list, which becomes the body of the email in another function
    Parameters:
    final_df (pd.DataFrame): The DataFrame to validate.
    Returns:
    errors (list): List of errors found during validation.
    '''

    errors = []
    # Check first if the input is a dataframe
    if not isinstance(final_df, pd.DataFrame):
        #raise ValueError("Input must be a pandas DataFrame.")
        errors.append("Input must be a pandas DataFrame.")
        
    
    # Check if all required columns are present
    required_columns = ['week_start_date','product_id','product_name','price_per_unit','total_sales','region','cpi_value','gas_value']
    for column in required_columns:
        if column not in final_df.columns:
            #raise ValueError(f"Missing required column: {column}")
            errors.append(f"Missing required column: {column}")
        

    # Check for missing values
    if final_df.isnull().values.any():
        #raise ValueError("Data contains missing values.")
        errors.append("Data contains missing values.")
    
    # Check for duplicates
    if final_df.duplicated().any():
        #raise ValueError("Data contains duplicate rows.")
        errors.append("Data contains duplicate rows.")
    

    #Check if data types are correct
    #Creating a dictionary of expected data type of each column   
    expected_types = {
        'week_start_date': 'datetime64[ns]',
        'product_id': 'int64',
        'product_name': 'object',
        'price_per_unit': 'float64',
        'total_sales': 'float64',
        'region': 'object',
        'cpi_value': 'float64',
        'gas_value': 'float64'
    }

    for column, expected_type in expected_types.items():
        if final_df[column].dtype != expected_type:
            #raise ValueError(f"Column {column} has incorrect type: expected {expected_type}, got {final_df[column].dtype}")
            errors.append(f"Column {column} has incorrect type: expected {expected_type}, got {final_df[column].dtype}")

    return errors
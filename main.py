from dotenv import load_dotenv
import os
import gas_api
import cpi_api
import generate_data
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Load environment variables from .env file
load_dotenv()


# # Check if the API key is loaded
# if api_key is None:
#     raise ValueError("API key not found. Please set the FRED_API environment variable.")



# # Fetching gas prices and CPI data
# # from FRED API

    # Generate mock sales data
# sales_df = generate_data.generate_sales_data()
    # Fetch gas price data from FRED API
# gas_df = gas_api.fetch_gas_prices(series_id=series_id_gas, api_key=api_key, observation_start=observation_start, observation_end=observation_end)
    # Fetch CPI data from FRED API
# cpi_df = cpi_api.fetch_consumer_price_index(series_id=series_id_cpi, api_key=api_key, observation_start=observation_start, observation_end=observation_end)


# # Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
    # Convert CPI date to datetime and extract month
# cpi_df['date'] = pd.to_datetime(cpi_df['date'])
# #cpi_df.set_index(cpi_df['date'], inplace=True)
# cpi_df['month'] = cpi_df['date'].dt.to_period('M')

# #sales_df['date'] = pd.to_datetime(sales_df['date'])
# sales_df['month'] = sales_df['date'].dt.to_period('M')

# #print(sales_df)
# #print(cpi_df)

# # Merge sales_df and cpi_df on month
    # Merge sales and CPI data on month
# merged_df = pd.merge(sales_df, cpi_df, on='month', how='inner')
# merged_df = merged_df.drop(columns=['month','date_y'])
# merged_df.rename(columns={'date_x': 'date','value':'cpi_value'}, inplace=True)

# # Now we have to obtain week number and create a new column for merged_df and gas_df
    # Convert gas price date to datetime and extract week number
# gas_df['date'] = pd.to_datetime(gas_df['date'])
# gas_df['week_num'] = gas_df['date'].dt.isocalendar().week
# merged_df['week_num'] = merged_df['date'].dt.isocalendar().week
# # Merge gas_df and merged_df on week_num
    # Merge combined sales+CPI data with gas price data on week number
# final_df = pd.merge(merged_df, gas_df, on='week_num', how='inner')
# final_df = final_df.drop(columns=['week_num','date_y'])
# final_df.rename(columns={'date_x': 'week_start_date','value':'gas_value'}, inplace=True)
# final_df.to_csv('data/final_data.csv', index=False)
# print(final_df)


# Convert the above process into a function
def fetch_and_merge_data(series_id_gas, series_id_cpi, observation_start, observation_end, api_key):
    # Fetching gas prices and CPI data
    # Generate mock sales data
    sales_df = generate_data.generate_sales_data()
    # Fetch gas price data from FRED API
    gas_df = gas_api.fetch_gas_prices(series_id=series_id_gas, api_key=api_key, observation_start=observation_start, observation_end=observation_end)
    # Fetch CPI data from FRED API
    cpi_df = cpi_api.fetch_consumer_price_index(series_id=series_id_cpi, api_key=api_key, observation_start=observation_start, observation_end=observation_end)

    # Convert cpi_data['date'] to datetime format, then convert from monthly to weekly
    # Convert CPI date to datetime and extract month
    cpi_df['date'] = pd.to_datetime(cpi_df['date'])
    cpi_df['month'] = cpi_df['date'].dt.to_period('M')

    # Conevert sales_df['date'] to datetime format
    #sales_df['date'] = pd.to_datetime(sales_df['date'])
    sales_df['month'] = sales_df['date'].dt.to_period('M')

    # Merge sales_df and cpi_df on month
    # Merge sales and CPI data on month
    merged_df = pd.merge(sales_df, cpi_df, on='month', how='inner')
    merged_df = merged_df.drop(columns=['month','date_y'])
    merged_df.rename(columns={'date_x': 'date','value':'cpi_value'}, inplace=True)

    # Now we have to obtain week number and create a new column for merged_df and gas_df
    # Convert gas price date to datetime and extract week number
    gas_df['date'] = pd.to_datetime(gas_df['date'])
    gas_df['week_num'] = gas_df['date'].dt.isocalendar().week
    merged_df['week_num'] = merged_df['date'].dt.isocalendar().week

    # Merge gas_df and merged_df on week_num
    # Merge combined sales+CPI data with gas price data on week number
    final_df = pd.merge(merged_df, gas_df, on='week_num', how='inner')
    final_df = final_df.drop(columns=['week_num','date_y'])
    final_df.rename(columns={'date_x': 'week_start_date','value':'gas_value'}, inplace=True)
    
    return final_df



# Validate the final DataFrame for required structure and consistency
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

    # Check for spikes in values of any columns
    threshold = 0.5  # Define a threshold for high change (e.g., 50%)
    numeric_columns = ['price_per_unit', 'total_sales', 'cpi_value', 'gas_value']

    for column in numeric_columns:
        if column in final_df.columns:
            # Calculate percentage change
            final_df[f'{column}_pct_change'] = final_df[column].pct_change()
            # Check for values exceeding the threshold
            if final_df[f'{column}_pct_change'].abs().max() > threshold:
                errors.append(f"High change detected in column {column}.")
            # Drop the temporary percentage change column
            final_df.drop(columns=[f'{column}_pct_change'], inplace=True)
            

    # Checking the data type of teh column
    for column, expected_type in expected_types.items():
        if final_df[column].dtype != expected_type:
            #raise ValueError(f"Column {column} has incorrect type: expected {expected_type}, got {final_df[column].dtype}")
            errors.append(f"Column {column} has incorrect type: expected {expected_type}, got {final_df[column].dtype}")

    return errors



# Send an alert email with validation errors if found
def send_email(errors):
    '''
    Send an email if data validation fails.
    Parameters:
    errors (list): List of errors to include in the email body.
    '''
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Data Validation Errors"

    body = "Data Validation Errors:\n\n" + "\n".join(errors)
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")




# Example usage

# Execute the main workflow when this script is run directly
if __name__ == "__main__":
    # FRED API details
    api_key = os.getenv("FRED_API")  # Replace with your actual API key
    series_id_gas = "GASREGW"
    series_id_cpi = "CPIAUCNS"
    observation_start = "2024-01-07"
    observation_end = "2024-12-24"

    # Fetch and merge data
    final_df = fetch_and_merge_data(series_id_gas, series_id_cpi, observation_start, observation_end, api_key)
    
    # Validate data
    errors = validate_data(final_df)
    
    # Send email if there are validation errors
    send_email(errors)
    # Save the final DataFrame to CSV
    final_df.to_csv('data/final_data_1.csv', index=False)

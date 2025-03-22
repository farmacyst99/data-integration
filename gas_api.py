
import requests
import pandas as pd
import json


# # FRED API details
# api_key = "bd7ee64d6749a1bd68c358548a4a8c81"
# series_id = "GASREGW"
# observation_start = "2024-01-07"
# observation_end = "2024-12-24"
# url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}&observation_end={observation_end}"

# # Fetch data from FRED API
# response = requests.get(url)
# if response.status_code == 200:
#     gas_data = response.json()["observations"]
#     # Convert to DataFrame
#     gas_df = pd.DataFrame(gas_data)
# else:
#     raise Exception(f"Failed to fetch data from FRED API: {response.status_code}")

# # Clean and process the data


# Saving to CSV
# print(gas_df.head())
# gas_df.to_csv("data/gas_data.csv", index=False)

# Function to fetch gas prices from FRED API
def fetch_gas_prices(api_key: str, series_id: str, observation_start: str, observation_end: str) -> pd.DataFrame:
    """
    Fetches gas prices from the FRED API and returns a DataFrame.
    
    Args:
        api_key (str): The API key for FRED.
        series_id (str): The series ID for the gas prices.
        observation_start (str): The start date for the observations. The date format should be YYYY-MM-DD.
        observation_end (str): The end date for the observations. The date format should be YYYY-MM-DD.
    
    Returns:
        pd.DataFrame: A DataFrame containing the gas prices data.
    """
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}&observation_end={observation_end}"
    response = requests.get(url)
    if response.status_code == 200:
        gas_data = response.json()["observations"]
        gas_df = pd.DataFrame(gas_data)
        gas_df = gas_df.drop(columns=['realtime_start', 'realtime_end'])
        return gas_df
    else:
        raise Exception(f"Failed to fetch data from FRED API: {response.status_code}")
    

# Function to save DataFrame to CSV
# def save_to_csv(df: pd.DataFrame, filename: str) -> None:
#     """
#     Saves a DataFrame to a CSV file.
    
#     Args:
#         df (pd.DataFrame): The DataFrame to save.
#         filename (str): The name of the CSV file.
#     """
#     new_df = pd.DataFrame()
#     new_df['date'] = df['date']
#     new_df['value'] = df['value']

#     new_df.to_csv(filename, index=False)
#     print(f"Data saved to {filename}")

# Running the functions
if __name__ == "__main__":
    # FRED API details
    api_key = "bd7ee64d6749a1bd68c358548a4a8c81"
    series_id = "GASREGW"
    observation_start = "2023-12-31"
    observation_end = "2024-12-24"
    # Fetch gas prices
    gas_df = fetch_gas_prices(api_key, series_id, observation_start, observation_end)
    # Save to CSV
    # save_to_csv(gas_df, "data/gas_data.csv")
    # Print the first few rows of the DataFrame
    print(gas_df.head())

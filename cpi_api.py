#! user/bin/python
import requests
import pandas as pd

def fetch_consumer_price_index(series_id: str, api_key: str, observation_start: str, observation_end: str) -> pd.DataFrame:
    """
    Fetches Consumer Price Index (CPI) data from the FRED API.
    
    Args:
        series_id (str): The series ID for the CPI data.
        api_key (str): The API key for FRED.
        observation_start (str): The start date for the observations in YYYY-MM-DD format.
        observation_end (str): The end date for the observations in YYYY-MM-DD format.
    
    Returns:
        pd.DataFrame: A DataFrame containing the CPI data.
    """
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={observation_start}&observation_end={observation_end}"
    response = requests.get(url)
    
    if response.status_code == 200:
        cpi_data = response.json()["observations"]
        cpi_df = pd.DataFrame(cpi_data)
        cpi_df = cpi_df.drop(columns=['realtime_start', 'realtime_end'])
        #cpi_df['date'] = pd.to_datetime(cpi_df['date'])
        #cpi_df['value'] = pd.to_numeric(cpi_df['value'], errors='coerce')
        #cpi_df['value'] = cpi_df['value'].astype(float)
        return cpi_df
    else:
        raise Exception(f"Failed to fetch data from FRED API: {response.status_code}")
    

# Save to CSV
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

# # Example usage
# if __name__ == "__main__":
#     # FRED API details
#     api_key = "your_api_key_here"  # Replace with your actual API key
#     series_id = "CPIAUCNS"
#     observation_start = "2024-01-07"
#     observation_end = "2024-12-24"
#     filename = "data/cpi_data.csv"
#     cpi_df = fetch_consumer_price_index(series_id, api_key, observation_start, observation_end)
#     # save_to_csv(cpi_df, filename)
#     print(cpi_df.info())
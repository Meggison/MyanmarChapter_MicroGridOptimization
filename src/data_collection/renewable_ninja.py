"""This script pulls data from the Renewable Ninja API.

Example usage:
    python renewable_ninja.py

Notes:
-   This script will not work without an API token.
-   The API token can be obtained from https://www.renewables.ninja/documentation/api
-   Change the parameters at the bottom of the script to suit your needs.
-   You will notice that many variables are hardcoded. Feel free to expose them as needed.
    However, at this time I do not feel that they are needed and the defaults should suffice for our use case.


"""
from time import sleep
import pandas as pd
import requests

# >> IMPORTANT: get your own token from https://www.renewables.ninja/documentation/api <<
# This script will not work without it!
API_TOKEN = "INSERT YOUR API TOKEN HERE"

BASE_URL = 'https://www.renewables.ninja/api/data'


def get_heating_demand(start_date, end_date, lat, lon):
    """Pulls daily demand data for a given location + time period.

    Args:
        start_date (str): start date in YYYY-MM-DD format
        end_date (str): end date in YYYY-MM-DD format
        lat (float): latitude
        lon (float): longitude

    Returns:
        dict: demand data
    """
    base_url = f"{BASE_URL}/demand"

    # Parameters for the API call
    params = {
        "local_time": "true",
        "lat": lat,
        "lon": lon,
        "date_from": start_date,
        "date_to": end_date,
        "dataset": "merra2",
        "heating_threshold": 14,
        "cooling_threshold": 20,
        "base_power": 0,
        "heating_power": 0.3,
        "cooling_power": 0.15,
        "smoothing": 0.5,
        "solar_gains": 0.012,
        "wind_chill": -0.2,
        "humidity_discomfort": 0.05,
        "use_diurnal_profile": "true",
        "format": "json",
        "mean": "day",
    }

    # Headers for the API call, including the authorization token
    headers = {"Authorization": f"Token {API_TOKEN}"}

    # Make the GET request to the API
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON data
        data = response.json()["data"]
        return data
    else:
        # Handle errors
        response.raise_for_status()


def get_pv_output(start_date, end_date, lat, lon):
    """Pulls hourly PV output for a given location + time period.

    Args:
        start_date (str): start date in YYYY-MM-DD format
        end_date (str): end date in YYYY-MM-DD format
        lat (float): latitude
        lon (float): longitude

    Returns:
        dict: unit PV output per hour, which assumes capacity of 1
    """
    base_url = f"{BASE_URL}/pv"

    # Parameters for the API call
    params = {
        "local_time": "true",
        "lat": lat,
        "lon": lon,
        "date_from": start_date,
        "date_to": end_date,
        "dataset": "merra2",
        "capacity": 1,
        "system_loss": 0.1,
        "tracking": 0,
        "tilt": 35,
        "azim": 180,
        "format": "json",
    }

    # Headers for the API call, including the authorization token
    headers = {"Authorization": f"Token {API_TOKEN}"}

    # Make the GET request to the API
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON data
        return response.json()["data"]
    else:
        # Handle errors
        response.raise_for_status()


def get_wind_output(start_date, end_date, lat, lon):
    """Pulls wind output for a given location + time period.

    Args:
        start_date (str): start date in YYYY-MM-DD format
        end_date (str): end date in YYYY-MM-DD format
        lat (float): latitude
        lon (float): longitude

    Returns:
        dict: unit wind output per hour, which assumes capacity of 1
    """
    base_url = f"{BASE_URL}/wind"

    # Parameters for the API call
    params = {
        "local_time": "true",
        "lat": lat,
        "lon": lon,
        "date_from": start_date,
        "date_to": end_date,
        "dataset": "merra2",
        "capacity": "1",
        "height": "80",
        "turbine": "Vestas V90 2000",
        "format": "json",
    }

    # Headers for the API call, including the authorization token
    headers = {"Authorization": f"Token {API_TOKEN}"}

    # Make the GET request to the API
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Return the JSON data
        return response.json()["data"]
    else:
        # Handle errors
        response.raise_for_status()


def pull_renewable_data(start_date, end_date, lat, lon, type):
    """
    Pulls data from the Renewable Ninja API.

    Args:
        start_date (str): start date in YYYY-MM-DD format
        end_date (str): end date in YYYY-MM-DD format
        lat (float): latitude
        lon (float): longitude
        type (str): 'pv', 'wind', or 'demand'

    Returns:
        pandas.DataFrame: data pulled from the API
    """
    data = {}

    if type == "pv":
        data = get_pv_output(start_date, end_date, lat, lon)
    elif type == "wind":
        data = get_wind_output(start_date, end_date, lat, lon)
    elif type == "demand":
        data = get_heating_demand(start_date, end_date, lat, lon)
        keys = data.keys()
        df = pd.DataFrame(data.values())
        df['date'] = keys
        return df
    return pd.DataFrame(data.values())


if __name__ == "__main__":
    PULL_TYPE = "wind"
    START_DATE = "2022-01-01"
    END_DATE = "2022-12-31"
    OUTPUT_DIR = "./"
    locations = [
        {"region": "Ayeyarwady", "lat": 17.1302, "lon": 94.9967},
        {"region": "Bago", "lat": 18.1781, "lon": 96.7663},
        {"region": "Chin", "lat": 24.4281, "lon": 94.9615},
        {"region": "Kachin", "lat": 26.7802, "lon": 97.5410},
        {"region": "Kayah", "lat": 19.5122, "lon": 97.4776},
        {"region": "Kayin", "lat": 16.6322, "lon": 98.2782},
        {"region": "Magway", "lat": 20.3436, "lon": 95.2739},
        {"region": "Mandalay", "lat": 21.9306, "lon": 95.9316},
        {"region": "Mon", "lat": 16.1933, "lon": 97.6669},
        {"region": "Naypyidaw Union", "lat": 19.9554, "lon": 96.2308},
        {"region": "Rakhine", "lat": 21.0099, "lon": 92.7589},
        {"region": "Sagaing", "lat": 24.5598, "lon": 95.3272},
        {"region": "Shan", "lat": 21.4148, "lon": 98.1206},
        {"region": "Tanintharyi", "lat": 13.1304, "lon": 98.8394},
        {"region": "Yangon", "lat": 17.2069, "lon": 95.9169},
    ]
    
    for location in locations:
        region, lat, lon = location["region"], location["lat"], location["lon"]
        print(region)
        file = f"{OUTPUT_DIR}/{PULL_TYPE}_{region}_{lat}_{lon}.csv"
        data = pull_renewable_data(START_DATE, END_DATE, lat, lon, PULL_TYPE)
        data.to_csv(file, index=False)
        sleep(15) # needed to respect the 4 request per minute rate limit

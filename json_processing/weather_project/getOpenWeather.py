#! /usr/bin/env python3
# getOpenWeather.py - Prints the weather for a location from the command line

import json
import requests
import sys
import os
from typing import Any, Dict

# ---------------------------------------------------------------------------- #
#                 API key from https://home.openweathermap.org/                #
# ---------------------------------------------------------------------------- #

def get_api_key() -> str:
    """
    Retrieve the API key from environment variables.

    Returns
    -------
    str
        The API key for the OpenWeatherMap service.
    """
    return os.environ['APPID']

# ---------------------------------------------------------------------------- #
#                 Compute location from command line arguments                 #
# ---------------------------------------------------------------------------- #

def get_location_from_args() -> str:
    """
    Compute location string from command line arguments.

    Returns
    -------
    str
        A single string representing the user-provided location.

    Raises
    ------
    SystemExit
        If no location is provided in the command line arguments, the program
        will print a usage message and exit.

    Notes
    -----
    This function expects city names and country codes to be provided as
    separate command line arguments. Example usage:
        $ python getOpenWeather.py Beijing CN
    This would set sys.argv to ['getOpenWeather.py', 'Beijing', 'CN']
    and the function would return 'Beijing CN'.
    """
    if len(sys.argv) < 2:
        print('Usage: getOpenWeather.py city_name, 2-letter_country_code')
        sys.exit(1)
    return ' '.join(sys.argv[1:])

# ---------------------------------------------------------------------------- #
#                              Download JSON data                              #
# ---------------------------------------------------------------------------- #

def download_weather_data(location: str, appid: str) -> Dict[str, Any]:
    """
    Download the JSON weather data from OpenWeatherMap's API.

    Parameters
    ----------
    location : str
        The location for which to retrieve weather data.
    appid : str
        The API key for authenticating with the OpenWeatherMap API.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the weather data.

    Raises
    ------
    HTTPError
        If an HTTP error occurs during API requests.
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={appid}'
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)

# ---------------------------------------------------------------------------- #
#                            Write to disk as .json                            #
# ---------------------------------------------------------------------------- #

def save_weather_data(weather_data: Dict[str, Any], filename: str) -> None:
    """
    Save the weather data to a JSON file.

    Parameters
    ----------
    weather_data : Dict[str, Any]
        The weather data to save.
    filename : str
        The filename under which to save the data.

    Notes
    -----
    The JSON data is saved in a readable format with sorted keys.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(weather_data, file, indent=4, separators=(", ", ": "), sort_keys=True)

# ---------------------------------------------------------------------------- #
#                                    Main                                      #
# ---------------------------------------------------------------------------- #

def main() -> None:
    """
    Main function to handle workflow.
    """
    appid = get_api_key()
    location = get_location_from_args()
    weather_data = download_weather_data(location, appid)
    save_weather_data(weather_data, 'beijing_weather.json')

if __name__ == "__main__":
    
    main()

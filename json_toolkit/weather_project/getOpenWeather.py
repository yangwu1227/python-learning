#! /usr/bin/env python3
# getOpenWeather.py - Prints the weather for a location from the command line

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

import json
import requests
import sys
import os
import pandas as pd

# ---------------------------------------------------------------------------- #
#                 API key from https://home.openweathermap.org/                #
# ---------------------------------------------------------------------------- #

# API key stored as a .txt file
# When first generating an API key, wait some time before becomes active
# Sometimes it throws a 401 'invalid api key' client error when making requests
with open('./api.txt', 'rt') as api:
    appid = api.read()

# ---------------------------------------------------------------------------- #
#                 Compute location from command line arguments                 #
# ---------------------------------------------------------------------------- #

# Arguments are stored in the sys.argv list
# If there is only one element in the list, then the user didn’t provide a location on the command line
# Print “usage” message to the user before the program ends
if len(sys.argv) < 2:
    print('Usage: getOpenWeather.py city_name, 2-letter_country_code')
    # Exit the interpreter by raising SystemExit(status)
    # If status is omitted or None, it defaults to zero (i.e., success)
    sys.exit()
# The command line argument 'Beijing', 'CN' make sys.argv hold ['getOpenWeather.py', 'Beijing,', 'CN']
# Join elements of sys.argv using a white space ' ', excluding element 0, 'getOpenWeather.py'
# For example, ['getOpenWeather.py', 'Beijing,', 'CN'] would return a str 'Beijing, CN'
location = ' '.join(sys.argv[1:])

# ---------------------------------------------------------------------------- #
#                              Download JSON data                              #
# ---------------------------------------------------------------------------- #

# Download the JSON data from OpenWeatherMap.org's API
# The global vars 'location' and 'APPID' are substituted for the '%s' placeholders in the url
url = 'https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s' % (
    location, appid)
# This returns a Response object
response = requests.get(url)
# Check for errors by calling the raise_for_status() method
# If not error, downloaded text should be stored in attribute response.text
response.raise_for_status()

# ---------------------------------------------------------------------------- #
#                                Load JSON data                                #
# ---------------------------------------------------------------------------- #

# Load JSON data into a Python dictionary object
weatherData = json.loads(s=response.text)

# ---------------------------------------------------------------------------- #
#                            Write to disk as .json                            #
# ---------------------------------------------------------------------------- #

with open('beijing_weather.json', 'wt', encoding='utf-8') as json_file:
    json.dump(weatherData, json_file, indent=4,
              separators=(", ", ": "), sort_keys=True)

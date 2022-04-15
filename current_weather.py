'''requests==2.27.1'''

'''This project is using OpenWeather API to extract current weather info.'''

import os
import requests
import re
from datetime import datetime


# Active API key stored in environment variables.
API_KEY = os.environ['current_weather_API_key']



# Variables needed for the while loop.
count = 0
attempt = ('First attmept', 'Second Attempt', 'Final Attempt')

# A loop that handles invalid input and gives 3 tries before closing the program.
while True:

    if count == 3:
        raise SystemExit

    # City name input and the API call
    city_name = input(f"({attempt[count]}) Enter city name to check it's current weather: ")
    api_call = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}'

    if city_name == '':
        print('A city name must be entered to proceed.')
        count += 1
        continue
    
    # API response from our request with extracting the information in a JSON file.
    api_json = requests.get(api_call).json()

    # using regex to make sure that the value of the 'cod' key in the json file repressents
    # a successful http status code 2XX, a client error status code 4XX, and a server error 5XX.
    pattern_successful = re.compile(r'[2]\d{2}')
    match_successful = pattern_successful.findall(str(api_json['cod']))
    pattern_unsuccessful = re.compile(r'[4]\d{2}|[5]\d{2}')
    match_unsuccessful = pattern_unsuccessful.findall(str(api_json['cod']))
    
    # As of the time of uplode of this project the 'cod' key is a string for invalid city name
    # and an integer for the valid city name. To resolve this issue I turn the value to an integer.
    if str(api_json['cod']) in match_unsuccessful:
        print('Invalid city name.')
        count += 1
        continue
    elif str(api_json['cod']) in match_successful:
        break

# A function extracting the desired data about the current weather in the given city.
def get_weather_info(OpenWeatherJSON: dict):
    country = api_json['sys']['country']
    weather_description = api_json['weather'][0]['description'].capitalize()
    temp = str(int(api_json['main']['temp'] - 273.15)) + ' °C'
    feels_like = str(int(api_json['main']['feels_like'] - 273.15)) + ' °C'
    min_temp = str(int(api_json['main']['temp_min'] - 273.15)) + ' °C'
    max_temp = str(int(api_json['main']['temp_max'] - 273.15)) + ' °C'
    pressure = str(api_json['main']['pressure']) + ' hPa'
    humidity = str(api_json['main']['humidity']) + ' %'
    date_time = datetime.now().strftime('%d/%m/%Y at %I:%M:%S %p')

    print(f'\nWeather information about {city_name.title()},{country} on {date_time}')
    print('-------------------------------------------------------------------------')
    print(f'Weather description: {weather_description}\n', end='')
    print(f'Temperature: {temp}\n', end='')
    print(f'Real feel temperature: {feels_like}\n', end='')
    print(f'Minimum temperature: {min_temp}\n', end='')
    print(f'Maximum temperature: {max_temp}\n', end='')
    print(f'Preasure: {pressure}\n', end='')
    print(f'Humidity: {humidity}\n', end='')

get_weather_info(api_json)
from datetime import datetime
import requests
from config import API_KEY, BASE_URL, city
from store_data import store_weather_data


def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "Imperial"}

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()

        city_name = weather_data.get("name")
        current_weather = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        min_temp = weather_data["main"]["temp_min"]
        max_temp = weather_data["main"]["temp_max"]
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        visibility = weather_data["visibility"]
        wind_speed = weather_data["wind"]["speed"]
        rain = weather_data.get("rain", {}).get("1h", 0)
        clouds = weather_data.get("clouds", {}).get("all", 0)
        description = weather_data["weather"][0]["description"]
        # time_of_data = weather_data["dt"]

        unix_timestamp = weather_data.get("dt")

        time_of_data = datetime.utcfromtimestamp(unix_timestamp)

        store_weather_data(city_name, current_weather, temperature, min_temp, max_temp,
                           pressure, humidity, visibility, wind_speed, rain, clouds,
                           description, time_of_data)

        return weather_data


    else:
        print(f"Error: {response.status_code}")
        return None

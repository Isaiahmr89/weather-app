import requests
import pytz
import schedule
import time
from datetime import datetime
from extract import fetch_weather
from store_data import store_weather_data


def scheduled_task():
    city = "Louisville"
    weather_data = fetch_weather(city)

    print(weather_data)

    if weather_data:
        if weather_data:
            # Unpack the dictionary into individual arguments
            rain = weather_data.get("rain", {}).get("1h", 0)
            clouds = weather_data.get("clouds", {}).get("all", 0)

            store_weather_data(
                weather_data['name'],
                weather_data['main'],
                weather_data['main']['temp'],
                weather_data['main']['temp_min'],
                weather_data['main']['temp_max'],
                weather_data['main']['pressure'],
                weather_data['main']['humidity'],
                weather_data['visibility'],
                weather_data['wind']['speed'],
                rain,
                clouds,
                weather_data['weather'][0]['description'],
                weather_data['dt']
            )


schedule.every(2).seconds.do(scheduled_task)

print("Starting auto weather collection...")

while True:
    schedule.run_pending()
    time.sleep(2)

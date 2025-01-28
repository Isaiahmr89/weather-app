from extract import fetch_weather
from src.config import city
from store_data import store_weather_data
from datetime import datetime
import pytz


if __name__ == '__main__':

    weather_data = fetch_weather(city)
    if weather_data:
        # Extract and print the fetched data for debugging
        print("Fetched Weather Data:")
        print(weather_data)

        city_name = weather_data.get("name")
        current_weather = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        min_temp = weather_data["main"]["temp_min"]
        max_temp = weather_data["main"]["temp_max"]
        pressure = weather_data["main"]["pressure"]
        humidity = weather_data["main"]["humidity"]
        visibility = weather_data.get("visibility", 10)  # Default to 10mi if missing
        wind_speed = weather_data["wind"]["speed"]
        rain = weather_data.get("rain", {}).get("1h", 0)  # Default to 0 if missing
        clouds = weather_data.get("clouds", {}).get("all", 0)  # Default to 0 if missing
        description = weather_data["weather"][0]["description"]
        unix_timestamp = weather_data.get("dt")

        if unix_timestamp is None:
            print("Error: unix_timestamp not found in the API response.")
        else:
            est = pytz.timezone('US/Eastern')
            time_of_data = datetime.fromtimestamp(unix_timestamp, est)

            # Call the store_weather_data function with extracted values
            print(f"Inserting Data for {city_name}...")
            store_weather_data(city_name, current_weather, temperature, min_temp, max_temp,
                               pressure, humidity, visibility, wind_speed, rain, clouds,
                               description, time_of_data)


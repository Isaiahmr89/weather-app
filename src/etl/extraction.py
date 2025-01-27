import requests
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_pass = os.getenv("db_pass")

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "standard"}

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
        clouds = weather_data["clouds"]["all"]
        description = weather_data["weather"][0]["description"]

        store_weather_data(city_name,
                           current_weather,
                           temperature,
                           min_temp,
                           max_temp,
                           pressure,
                           humidity,
                           visibility,
                           wind_speed,
                           rain,
                           clouds,
                           description
                           )

    else:
        print(f"Error: {response.status_code}")
        return None

def store_weather_data(city_name,
                       current_weather,
                       temperature,
                       min_temp,
                       max_temp,
                       pressure,
                       humidity,
                       visibility,
                       wind_speed,
                       rain,
                       clouds,
                       description
                       ):
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass
        )
        cursor = conn.cursor()

        insert_query = """INSERT INTO weather_data (city_name,
                       current_weather,
                       temperature,
                       min_temp,
                       max_temp,
                       pressure,
                       humidity,
                       visibility,
                       wind_speed,
                       rain,
                       clouds,
                       description)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                       """
        cursor.execute(insert_query, (city_name,
                       current_weather,
                       temperature,
                       min_temp,
                       max_temp,
                       pressure,
                       humidity,
                       visibility,
                       wind_speed,
                       rain,
                       clouds,
                       description))

        conn.commit()
        print(f"Weather data from {city_name} has been inserted into the database.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"There was an Error inserting data into the database {e}")


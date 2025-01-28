import psycopg2
from datetime import datetime
from config import db_host, db_user, db_name, db_pass
import logging


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
                       description,
                       time_of_data
                       ):
    try:

        rain = rain if isinstance(rain, (int, float)) else 0
        clouds = clouds.get('all', 0) if isinstance(clouds, dict) else 0
        description = description if isinstance(description, str) else ""
        wind_speed = wind_speed if isinstance(wind_speed, (int, float)) else 0
        visibility = visibility if isinstance(visibility, int) else 0

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
                       description,
                       time_of_data)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
                                      description,
                                      time_of_data))

        conn.commit()
        print(f"Weather data from {city_name} has been inserted into the database.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"There was an Error inserting data into the database {e}")

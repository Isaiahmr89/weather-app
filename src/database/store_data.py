from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(DB_URL)


def store_weather(data):
    df = pd.DataFrame([data])
    df.to_sql("weather_data", engine, if_exists="append", index=False)

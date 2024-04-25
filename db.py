import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
from dotenv import load_dotenv


def connect_to_db():
    load_dotenv()
    try:
        # Replace 'dbname', 'user', 'password', and 'host' with your database details
        connection = psycopg2.connect(
            dbname= os.getenv('DBNAME'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            host=os.getenv('HOST')
        )
        connection.autocommit = True
        print("Connected to the database successfully")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")

def insert_weather_data(db_connection, weather_data):
    cursor = db_connection.cursor()

    cursor.execute("DELETE FROM weather_forecasts;")
    print("Existing data cleared from table.")

    query = """
    INSERT INTO weather_forecasts (period, short_desc, temperature)
    VALUES (%s, %s, %s);
    """
    for data in weather_data:
        cursor.execute(query, (data['period'], data['short_desc'], data['temp']))
    print("Data inserted successfully")

def fetch_data(db_connection):
    cursor = db_connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM weather_forecasts;")
    records = cursor.fetchall()
    for record in records:
        print(record)

def fetch_data_to_dataframe(connection):
    query = "SELECT * FROM weather_forecasts;"
    dataframe = pd.read_sql_query(query, connection)
    return dataframe


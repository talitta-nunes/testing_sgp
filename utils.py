from dotenv import load_dotenv
import os
import mysql.connector

def connect_to_mysql():
    load_dotenv()
    host = os.getenv('DB_HOST')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    port = 3306

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        return conn
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
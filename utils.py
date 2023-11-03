from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
port=3306

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    port=3306
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE sgp")

cursor.close()
conn.close()

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

def get_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_recommender"),
        auth_plugin="mysql_native_password"
    )
    return connection

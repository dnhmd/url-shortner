from contextlib import contextmanager
from dotenv import load_dotenv
import os

import psycopg2

load_dotenv()

HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")

@contextmanager
def get_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        yield conn
    except psycopg2.Error as error:
        print(f"Database error: {error}")
        raise
    finally:
        if conn:
            conn.close()
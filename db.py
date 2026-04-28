from contextlib import contextmanager
import os

import psycopg2

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

@contextmanager
def get_connection():
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="urlshortner",
            user="postgres",
            password=POSTGRES_PASSWORD,
            port=5432
        )
        yield conn
    except psycopg2.Error as error:
        print(f"Database error: {error}")
        raise
    finally:
        if conn:
            conn.close()
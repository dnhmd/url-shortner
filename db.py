from contextlib import contextmanager
from dotenv import load_dotenv
import os

import psycopg2

load_dotenv()

HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
PORT = os.getenv("DB_PORT")

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

def insert_resource(alias, source):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("insert into aliases(alias, source) values (%s, %s) returning id, alias, created_at;", (alias, source))
            result = cur.fetchone()
        conn.commit()

    return result

def get_source(alias):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("select source from aliases where alias = %s;", (alias,))
            result = cur.fetchone()
    
    return result
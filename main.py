from db import get_connection

with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"You are connected to: {version[0]}")
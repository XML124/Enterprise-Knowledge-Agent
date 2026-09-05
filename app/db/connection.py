import time, psycopg
from pgvector.psycopg import register_vector
from app.core.config import get_settings

def get_connection(retries=10, delay_seconds=1.0):
    last = None
    for _ in range(retries):
        try:
            conn = psycopg.connect(get_settings().database_url)
            register_vector(conn)
            return conn
        except Exception as exc:
            last = exc
            time.sleep(delay_seconds)
    raise RuntimeError("Could not connect to PostgreSQL") from last

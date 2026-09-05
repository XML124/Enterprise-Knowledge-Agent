from app.core.config import get_settings
from app.db.connection import get_connection

def initialise_database():
    s = get_settings()
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                source TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                embedding VECTOR({s.embedding_dim}) NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                UNIQUE(source, chunk_index)
            );
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_documents_source ON documents(source);")
    conn.commit(); conn.close()

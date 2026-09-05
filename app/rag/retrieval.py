from app.db.connection import get_connection
from app.providers.embeddings import get_embedding_provider

def retrieve(query: str, top_k: int = 4) -> list[dict]:
    emb = get_embedding_provider().embed(query)
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT source, chunk_index, content, 1-(embedding <=> %s) AS similarity
            FROM documents
            ORDER BY embedding <=> %s
            LIMIT %s
        """, (emb, emb, top_k))
        rows = cur.fetchall()
    conn.close()
    return [
        {"source": r[0], "chunk_index": r[1], "content": r[2], "similarity": float(r[3])}
        for r in rows
    ]

def list_sources() -> list[str]:
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT source FROM documents ORDER BY source")
        rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]

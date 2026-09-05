from app.db.connection import get_connection
from app.providers.embeddings import get_embedding_provider
from app.rag.chunking import chunk_text

def ingest_text(source: str, text: str) -> int:
    chunks = chunk_text(text)
    provider = get_embedding_provider()
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM documents WHERE source=%s", (source,))
        for i, chunk in enumerate(chunks):
            cur.execute(
                "INSERT INTO documents(source,chunk_index,content,embedding) VALUES (%s,%s,%s,%s)",
                (source, i, chunk, provider.embed(chunk)),
            )
    conn.commit(); conn.close()
    return len(chunks)

import pytest
from app.rag.chunking import chunk_text

def test_chunking_returns_content():
    chunks = chunk_text("a " * 1000, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(c.strip() for c in chunks)

def test_chunk_size_must_exceed_overlap():
    with pytest.raises(ValueError):
        chunk_text("abc", chunk_size=100, overlap=100)

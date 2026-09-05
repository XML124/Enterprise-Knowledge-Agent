from app.providers.embeddings import DeterministicEmbeddingProvider

def test_mock_embedding_is_deterministic():
    p = DeterministicEmbeddingProvider(64)
    assert p.embed("cooling pump pressure") == p.embed("cooling pump pressure")
    assert len(p.embed("cooling pump pressure")) == 64

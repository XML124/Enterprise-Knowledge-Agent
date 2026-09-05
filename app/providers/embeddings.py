import hashlib, math
from abc import ABC, abstractmethod
from openai import OpenAI
from app.core.config import get_settings

class EmbeddingProvider(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...

class DeterministicEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dim): self.dim = dim
    def embed(self, text):
        vec = [0.0] * self.dim
        for token in text.lower().split():
            d = hashlib.sha256(token.encode()).digest()
            i = int.from_bytes(d[:4], "big") % self.dim
            vec[i] += 1.0 if d[4] % 2 == 0 else -1.0
        norm = math.sqrt(sum(x*x for x in vec)) or 1.0
        return [x / norm for x in vec]

class OpenAIEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        s = get_settings()
        if not s.openai_api_key: raise ValueError("OPENAI_API_KEY required")
        self.client = OpenAI(api_key=s.openai_api_key)
        self.model = s.openai_embedding_model
    def embed(self, text):
        return self.client.embeddings.create(model=self.model, input=text).data[0].embedding

def get_embedding_provider():
    s = get_settings()
    return OpenAIEmbeddingProvider() if s.app_mode.lower() == "openai" else DeterministicEmbeddingProvider(s.embedding_dim)

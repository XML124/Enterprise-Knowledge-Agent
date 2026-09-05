from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

class SourceReference(BaseModel):
    source: str
    chunk_index: int

class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference]

class IngestResponse(BaseModel):
    filename: str
    chunks_created: int

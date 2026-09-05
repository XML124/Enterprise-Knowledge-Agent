import logging
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.agent.graph import ask_agent
from app.core.config import get_settings
from app.rag.ingest import ingest_text
from app.rag.retrieval import list_sources
from app.schemas.api import IngestResponse, QueryRequest, QueryResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
def health():
    return {"status": "ok", "mode": get_settings().app_mode}

@router.get("/documents")
def documents():
    return {"documents": list_sources()}

@router.post("/documents", response_model=IngestResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise HTTPException(400, "This learning version accepts .txt files only")
    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(400, "File must be UTF-8") from exc
    if not text.strip():
        raise HTTPException(400, "Document is empty")
    chunks = ingest_text(file.filename, text)
    logger.info("document_ingested filename=%s chunks=%s", file.filename, chunks)
    return IngestResponse(filename=file.filename, chunks_created=chunks)

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = ask_agent(req.question)
    logger.info("query_completed question_length=%s", len(req.question))
    return QueryResponse(**result)

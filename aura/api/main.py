from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from aura.core.config import settings
from aura.ingestion.chunker import chunk_text
from aura.ingestion.parser import SUPPORTED_EXTENSIONS, parse_document
from aura.retrieval.bm25 import BM25Retriever

app = FastAPI(title=settings.app_name,
              description="Local-first research document ingestion and retrieval API.",
              version="0.1.0")
retriever = BM25Retriever()
_chunks = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@app.get("/stats")
def stats() -> dict[str, int | str]:
    return {"indexed_chunks": retriever.size,
            "documents": len({chunk.document_id for chunk in _chunks})}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    filename = Path(file.filename or "upload.txt").name
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"Supported file types: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")
    content = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(content) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, "File exceeds configured upload limit")
    temp_path = None
    try:
        with NamedTemporaryFile(suffix=suffix, delete=False) as temp:
            temp.write(content)
            temp_path = Path(temp.name)
        extracted = parse_document(temp_path)
    except Exception as exc:
        raise HTTPException(400, f"Could not parse document: {exc}") from exc
    finally:
        if temp_path:
            temp_path.unlink(missing_ok=True)
    if not extracted:
        raise HTTPException(400, "No extractable text found in document")
    document_id = Path(filename).stem.replace(" ", "_")[:80]
    new_chunks = chunk_text(extracted, document_id, filename,
                            settings.chunk_size, settings.chunk_overlap)
    existing_ids = {chunk.chunk_id for chunk in _chunks}
    _chunks.extend(chunk for chunk in new_chunks if chunk.chunk_id not in existing_ids)
    retriever.fit(_chunks)
    return {"source": filename, "chunks_added": len(new_chunks), "total_chunks": retriever.size}


@app.get("/search")
def search(q: str = Query(min_length=1, max_length=1000),
           top_k: int = Query(default=5, ge=1, le=20)) -> dict:
    results = retriever.search(q, top_k=top_k)
    return {"query": q, "count": len(results), "results": [item.to_dict() for item in results]}

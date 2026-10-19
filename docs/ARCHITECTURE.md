# Architecture

## Implemented
- PDF/TXT/Markdown parsing
- Character-window chunking with source metadata
- BM25 keyword retrieval
- Recall@k, reciprocal rank, and nDCG@k helpers
- FastAPI health, stats, ingest, and search endpoints
- Streamlit UI

## Limitations
- Index is in-memory and resets on API restart.
- Document IDs currently derive from filenames and may collide.
- Dense retrieval, hybrid fusion, reranking, and generation are not implemented yet.
- Scanned PDFs need OCR, which is not included.
- Authentication and public deployment hardening are not included.

## Planned experiment
Compare BM25, dense retrieval, hybrid retrieval, and hybrid + reranking on a fixed labelled query set. Report Recall@k, MRR, nDCG@k, latency, and index build time.

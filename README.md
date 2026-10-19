# AURA — AI Understanding, Retrieval & Analysis

AURA is an open-source, local-first research assistant and retrieval evaluation toolkit. This starter includes document ingestion, overlapping chunking, a BM25 search baseline, evaluation metrics, a FastAPI API, a Streamlit UI, tests, and GitHub CI.

**Status:** Initial scaffold. Dense retrieval, reranking, and answer generation are planned—not claimed as implemented.

## Features
- PDF, TXT, and Markdown ingestion
- Stable chunk IDs and source metadata
- BM25 keyword retrieval
- Recall@k, reciprocal rank, and nDCG@k metrics
- FastAPI REST endpoints and Streamlit dashboard
- Tests, Ruff linting, and GitHub Actions
- No paid API keys required

## Quick start (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn aura.api.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

In a second terminal:
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run dashboard/app.py
```

## Use
Upload a PDF, TXT, or Markdown file in the dashboard, then search its indexed text. Or call:
```powershell
Invoke-RestMethod "http://127.0.0.1:8000/search?q=transformer%20attention&top_k=5"
```

Run checks:
```powershell
pytest
ruff check .
```

## Roadmap
- [x] Document parsing and chunking
- [x] BM25 baseline
- [x] Retrieval metrics and tests
- [x] API and dashboard starter
- [ ] Dense embeddings with Sentence Transformers + FAISS
- [ ] Hybrid retrieval and cross-encoder reranking
- [ ] Local LLM answers with evidence citations
- [ ] Reproducible benchmark report and experiment tracking
- [ ] Docker, authentication, observability, and deployment hardening

## Important limitations
The index is in-memory and resets when the API restarts. Scanned PDFs need OCR, which is not included. Authentication and public deployment hardening are not included. Do not claim performance improvements until controlled experiments demonstrate them.

## License
MIT — see `LICENSE`.

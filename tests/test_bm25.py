from aura.ingestion.chunker import chunk_text
from aura.retrieval.bm25 import BM25Retriever, tokenize


def test_tokenize_case_insensitive():
    assert tokenize("Python PYTHON") == ["python", "python"]


def test_bm25_retrieves_relevant_chunk():
    chunks = (chunk_text("Python is a programming language.", "a", "a.txt", 100, 0)
              + chunk_text("Bananas are yellow fruit.", "b", "b.txt", 100, 0))
    retriever = BM25Retriever()
    retriever.fit(chunks)
    results = retriever.search("Python programming", top_k=2)
    assert results and results[0].document_id == "a"


def test_empty_index():
    assert BM25Retriever().search("anything") == []

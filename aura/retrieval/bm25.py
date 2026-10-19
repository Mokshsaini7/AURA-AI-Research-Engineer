import re
from dataclasses import asdict, dataclass

from rank_bm25 import BM25Okapi
from aura.ingestion.chunker import Chunk

_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+|[^\W\d_]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_PATTERN.findall(text)]


@dataclass(frozen=True, slots=True)
class SearchResult:
    chunk_id: str
    document_id: str
    source: str
    text: str
    score: float

    def to_dict(self) -> dict:
        return asdict(self)


class BM25Retriever:
    """Small in-memory BM25 baseline for local experiments."""

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._index: BM25Okapi | None = None

    @property
    def size(self) -> int:
        return len(self._chunks)

    def fit(self, chunks: list[Chunk]) -> None:
        self._chunks = list(chunks)
        tokenized = [tokenize(chunk.text) for chunk in self._chunks]
        self._index = BM25Okapi(tokenized) if any(tokenized) else None

    def search(self, query: str, top_k: int = 5) -> list[SearchResult]:
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if not query.strip() or not self._chunks or self._index is None:
            return []
        scores = self._index.get_scores(tokenize(query))
        ranked = sorted(enumerate(scores), key=lambda pair: pair[1], reverse=True)
        return [
            SearchResult(self._chunks[i].chunk_id, self._chunks[i].document_id,
                         self._chunks[i].source, self._chunks[i].text, float(score))
            for i, score in ranked[:top_k] if score > 0
        ]

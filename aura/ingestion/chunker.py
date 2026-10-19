from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chunk:
    chunk_id: str
    document_id: str
    source: str
    text: str
    start_char: int
    end_char: int


def chunk_text(text: str, document_id: str, source: str,
               chunk_size: int = 900, overlap: int = 150) -> list[Chunk]:
    """Split text into overlapping character windows with stable IDs."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")
    cleaned = " ".join(text.split())
    if not cleaned:
        return []
    chunks = []
    step = chunk_size - overlap
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        content = cleaned[start:end].strip()
        if content:
            chunks.append(Chunk(
                chunk_id=f"{document_id}:chunk{len(chunks)}",
                document_id=document_id, source=source, text=content,
                start_char=start, end_char=end,
            ))
        if end == len(cleaned):
            break
        start += step
    return chunks

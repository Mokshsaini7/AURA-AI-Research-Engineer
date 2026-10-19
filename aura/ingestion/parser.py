from pathlib import Path
from pypdf import PdfReader

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def parse_document(path: str | Path) -> str:
    """Extract text from a supported local document."""
    file_path = Path(path)
    suffix = file_path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {suffix}")
    if suffix in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8", errors="replace").strip()
    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(text.strip() for text in pages if text.strip()).strip()

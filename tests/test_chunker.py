import pytest
from aura.ingestion.chunker import chunk_text


def test_chunk_text_returns_stable_ids_and_overlap():
    chunks = chunk_text("abcdefghij", "doc", "file.txt", chunk_size=6, overlap=2)
    assert [item.chunk_id for item in chunks] == ["doc:chunk0", "doc:chunk1"]
    assert chunks[0].text == "abcdef"
    assert chunks[1].text == "efghij"


def test_empty_text_returns_no_chunks():
    assert chunk_text("  ", "doc", "file.txt") == []


@pytest.mark.parametrize("size,overlap", [(0, 0), (5, 5), (5, -1)])
def test_invalid_settings_raise(size, overlap):
    with pytest.raises(ValueError):
        chunk_text("hello world", "doc", "file.txt", size, overlap)

from fastapi.testclient import TestClient
from aura.api.main import app, retriever, _chunks

client = TestClient(app)


def setup_function():
    _chunks.clear()
    retriever.fit([])


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_search_empty_index():
    response = client.get("/search", params={"q": "anything"})
    assert response.status_code == 200
    assert response.json()["count"] == 0

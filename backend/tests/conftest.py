import os

import pytest
from fastapi.testclient import TestClient


class _FakeCollection:
    """Mimics the subset of the chromadb Collection API used by the
    document routes (`collection.get(where=..., include=...)`)."""

    def __init__(self, docs: dict):
        self._docs = docs

    def get(self, where=None, include=None):
        metadatas = []
        for doc_id, chunk_metas in self._docs.items():
            if where and where.get("doc_id") not in (None, doc_id):
                continue
            metadatas.extend(chunk_metas)
        return {"metadatas": metadatas}


class FakeVectorStore:
    """In-memory stand-in for VectorStoreRepository so tests don't need
    chromadb installed."""

    def __init__(self):
        self._docs: dict[str, list[dict]] = {}
        self._collection = _FakeCollection(self._docs)

    def add_document(self, doc_id: str, chunks: list[str], filename: str) -> int:
        if not chunks:
            return 0
        self._docs[doc_id] = [
            {"doc_id": doc_id, "document": filename, "chunk_index": i}
            for i in range(len(chunks))
        ]
        return len(chunks)

    def delete_document(self, doc_id: str) -> None:
        self._docs.pop(doc_id, None)

    def count_documents(self) -> int:
        return len(self._docs)

    def list_document_ids(self) -> list[str]:
        return list(self._docs.keys())

    def search(
        self, query: str, top_k: int = 4, document_ids: list[str] | None = None,
    ) -> list[dict]:
        return []


@pytest.fixture
def temp_chroma(tmp_path):
    os.environ["CHROMA_PERSIST_DIR"] = str(tmp_path / "chroma_test")
    os.environ["HUGGINGFACE_API_TOKEN"] = "test-token"
    yield str(tmp_path / "chroma_test")


@pytest.fixture
def client(temp_chroma):
    from app.config import Settings
    from app.main import create_app

    settings = Settings()
    fake_store = FakeVectorStore()
    app = create_app(settings=settings, vector_store=fake_store)
    return TestClient(app)

import tempfile
import pytest
from app.repositories.vector_store import VectorStoreRepository


@pytest.fixture
def repo(tmp_path):
    return VectorStoreRepository(
        persist_dir=str(tmp_path / "chroma"),
        embedding_model="all-MiniLM-L6-v2",
    )


def test_add_document(repo):
    chunks = ["First chunk of text.", "Second chunk of text."]
    count = repo.add_document("doc-1", chunks, "test.pdf")
    assert count == 2


def test_count_documents(repo):
    assert repo.count_documents() == 0
    repo.add_document("doc-1", ["chunk one"], "a.pdf")
    assert repo.count_documents() == 1
    repo.add_document("doc-2", ["chunk two"], "b.pdf")
    assert repo.count_documents() == 2


def test_search_returns_results(repo):
    repo.add_document("doc-1", [
        "Python is a programming language.",
        "JavaScript runs in the browser.",
        "Rust is a systems programming language.",
    ], "languages.txt")
    results = repo.search("What is Python?", top_k=2)
    assert len(results) <= 2
    assert all("content" in r and "document" in r for r in results)


def test_search_filters_by_document_ids(repo):
    repo.add_document("doc-1", ["Python is great."], "a.txt")
    repo.add_document("doc-2", ["JavaScript is great."], "b.txt")
    results = repo.search("great language", top_k=4, document_ids=["doc-1"])
    assert all(r["document"] == "a.txt" for r in results)


def test_delete_document(repo):
    repo.add_document("doc-1", ["chunk one", "chunk two"], "a.pdf")
    assert repo.count_documents() == 1
    repo.delete_document("doc-1")
    assert repo.count_documents() == 0


def test_list_document_ids(repo):
    repo.add_document("doc-1", ["chunk"], "a.pdf")
    repo.add_document("doc-2", ["chunk"], "b.pdf")
    ids = repo.list_document_ids()
    assert set(ids) == {"doc-1", "doc-2"}

from unittest.mock import MagicMock

from app.services.retriever import RetrieverService, build_prompt


def test_build_prompt_includes_context_and_question():
    chunks = [
        {"content": "Python is great.", "document": "a.txt", "chunk_index": 0},
        {"content": "Java is verbose.", "document": "b.txt", "chunk_index": 0},
    ]
    prompt = build_prompt(chunks, "What is Python?")
    assert "Python is great." in prompt
    assert "What is Python?" in prompt
    assert "Java is verbose." in prompt


def test_build_prompt_with_empty_chunks():
    prompt = build_prompt([], "question?")
    assert "question?" in prompt


def test_retriever_query_returns_sources():
    mock_repo = MagicMock()
    mock_repo.search.return_value = [
        {"content": "Python is great.", "document": "a.txt", "chunk_index": 0},
    ]
    mock_llm = MagicMock()
    mock_llm.generate_stream.return_value = iter(["Hello", " world"])

    service = RetrieverService(repo=mock_repo, llm=mock_llm, top_k=4)
    token_stream, sources = service.query("What is Python?")
    tokens = list(token_stream)
    assert tokens == ["Hello", " world"]
    assert len(sources) == 1
    assert sources[0]["document"] == "a.txt"


def test_retriever_query_filters_by_document_ids():
    mock_repo = MagicMock()
    mock_repo.search.return_value = []
    mock_llm = MagicMock()
    mock_llm.generate_stream.return_value = iter([])

    service = RetrieverService(repo=mock_repo, llm=mock_llm, top_k=4)
    service.query("question?", document_ids=["doc-1"])
    mock_repo.search.assert_called_once_with("question?", top_k=4, document_ids=["doc-1"])

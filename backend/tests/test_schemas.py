from app.models.schemas import (
    ChatRequest,
    ChatTokenEvent,
    ChatSourcesEvent,
    ChatErrorEvent,
    DocumentResponse,
    HealthResponse,
    SourceInfo,
)


def test_document_response_fields():
    doc = DocumentResponse(id="abc-123", filename="report.pdf", chunks=42, created_at="2026-01-01T00:00:00Z")
    assert doc.id == "abc-123"
    assert doc.filename == "report.pdf"
    assert doc.chunks == 42


def test_chat_request_defaults():
    req = ChatRequest(question="What is this?")
    assert req.question == "What is this?"
    assert req.document_ids is None


def test_chat_request_with_doc_ids():
    req = ChatRequest(question="Summarize", document_ids=["id1", "id2"])
    assert req.document_ids == ["id1", "id2"]


def test_chat_token_event():
    event = ChatTokenEvent(token="Hello")
    assert event.token == "Hello"


def test_chat_sources_event():
    source = SourceInfo(document="file.pdf", excerpt="some text")
    event = ChatSourcesEvent(sources=[source])
    assert len(event.sources) == 1
    assert event.sources[0].document == "file.pdf"


def test_chat_error_event():
    event = ChatErrorEvent(message="Rate limited")
    assert event.message == "Rate limited"


def test_health_response():
    health = HealthResponse(status="ok", model="Mistral-7B", documents_count=5)
    assert health.status == "ok"
    assert health.documents_count == 5

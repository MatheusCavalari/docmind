from unittest.mock import MagicMock, patch


def test_chat_returns_sse_stream(client):
    # Upload a document first
    import io
    file = io.BytesIO(b"Python is a programming language used for many things.")
    client.post("/api/documents", files={"file": ("test.txt", file, "text/plain")})

    mock_llm = MagicMock()
    mock_llm.generate_stream.return_value = iter(["Python ", "is ", "great."])

    with patch("app.api.chat.get_retriever_service") as mock_get:
        from app.services.retriever import RetrieverService
        real_retriever = RetrieverService.__new__(RetrieverService)
        real_retriever._repo = None
        real_retriever._llm = mock_llm
        real_retriever._top_k = 4

        def fake_query(question, document_ids=None):
            sources = [{"document": "test.txt", "excerpt": "Python is a..."}]
            return iter(["Python ", "is ", "great."]), sources

        mock_service = MagicMock()
        mock_service.query = fake_query
        mock_get.return_value = mock_service

        response = client.post(
            "/api/chat",
            json={"question": "What is Python?"},
            headers={"Accept": "text/event-stream"},
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers["content-type"]

        lines = response.text.strip().split("\n")
        events = []
        current_event = {}
        for line in lines:
            if line.startswith("event:"):
                current_event["event"] = line.split(":", 1)[1].strip()
            elif line.startswith("data:"):
                current_event["data"] = line.split(":", 1)[1].strip()
                events.append(current_event)
                current_event = {}

        event_types = [e["event"] for e in events]
        assert "token" in event_types
        assert "sources" in event_types
        assert "done" in event_types

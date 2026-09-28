import json
from collections.abc import AsyncIterator

from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse

from app.models.schemas import ChatRequest

router = APIRouter(prefix="/api")


def get_retriever_service():
    from app.main import _retriever_service
    return _retriever_service


async def _stream_response(question: str, document_ids: list[str] | None) -> AsyncIterator[dict]:
    retriever = get_retriever_service()
    try:
        token_stream, sources = retriever.query(question, document_ids=document_ids)
        for token in token_stream:
            yield {"event": "token", "data": json.dumps({"token": token})}
        yield {
            "event": "sources",
            "data": json.dumps({"sources": sources}),
        }
        yield {"event": "done", "data": json.dumps({})}
    except Exception as e:
        error_msg = str(e)
        if "rate" in error_msg.lower() or "429" in error_msg:
            error_msg = "Rate limit exceeded. Try again in a few seconds."
        yield {"event": "error", "data": json.dumps({"message": error_msg})}


@router.post("/chat")
async def chat(request: ChatRequest):
    return EventSourceResponse(
        _stream_response(request.question, request.document_ids)
    )

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    chunks: int
    created_at: str


class ChatRequest(BaseModel):
    question: str
    document_ids: list[str] | None = None


class SourceInfo(BaseModel):
    document: str
    excerpt: str


class ChatTokenEvent(BaseModel):
    token: str


class ChatSourcesEvent(BaseModel):
    sources: list[SourceInfo]


class ChatErrorEvent(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: str
    model: str
    documents_count: int

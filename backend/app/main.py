from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import Settings
from app.models.schemas import HealthResponse
from app.services.ingest import IngestService
from app.services.llm import LLMService
from app.services.retriever import RetrieverService

_vector_store = None
_ingest_service = None
_retriever_service = None


def create_app(
    settings: Settings | None = None,
    vector_store=None,
    ingest_service=None,
    retriever_service=None,
) -> FastAPI:
    """Build the DocMind FastAPI app.

    Production callers (or `app = create_app()` below) let this wire up the
    real chromadb-backed VectorStoreRepository. Tests can inject fakes via
    `vector_store` / `ingest_service` / `retriever_service` to avoid needing
    chromadb installed.
    """
    global _vector_store, _ingest_service, _retriever_service

    if settings is None:
        settings = Settings()

    if vector_store is not None:
        _vector_store = vector_store
    else:
        # Imported lazily so importing this module never requires chromadb
        # to be installed unless a real app is actually being constructed.
        from app.repositories.vector_store import VectorStoreRepository

        _vector_store = VectorStoreRepository(
            persist_dir=settings.chroma_persist_dir,
            embedding_model=settings.embedding_model,
        )

    _ingest_service = ingest_service or IngestService(
        repo=_vector_store,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )

    if retriever_service is not None:
        _retriever_service = retriever_service
    else:
        llm = LLMService(api_token=settings.huggingface_api_token, model=settings.llm_model)
        _retriever_service = RetrieverService(
            repo=_vector_store, llm=llm, top_k=settings.top_k
        )

    app = FastAPI(title="DocMind", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.documents import router as documents_router
    app.include_router(documents_router)

    from app.api.chat import router as chat_router
    app.include_router(chat_router)

    @app.get("/api/health", response_model=HealthResponse)
    async def health():
        return HealthResponse(
            status="ok",
            model=settings.llm_model,
            documents_count=_vector_store.count_documents() if _vector_store else 0,
        )

    return app


try:
    # Real deployments (with chromadb installed) get a ready-to-serve app
    # object for `uvicorn app.main:app`. In environments without chromadb
    # (e.g. local dev without the vector store deps), this is skipped and
    # `create_app()` can still be called explicitly with injected services.
    app = create_app()
except Exception:
    app = None

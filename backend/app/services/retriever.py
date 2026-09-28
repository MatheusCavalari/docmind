from collections.abc import Iterator
from typing import TYPE_CHECKING

from app.services.llm import LLMService

if TYPE_CHECKING:
    from app.repositories.vector_store import VectorStoreRepository


PROMPT_TEMPLATE = (
    "You are a helpful assistant that answers questions based on the provided documents.\n"
    "Use ONLY the information from the documents below to answer. If the answer is not\n"
    'in the documents, say "I could not find this information in the provided documents."'
    "\n\nDocuments:\n---\n{context}\n---\n\nQuestion: {question}"
)


def build_prompt(chunks: list[dict], question: str) -> str:
    context_parts = []
    for chunk in chunks:
        context_parts.append(f"[{chunk['document']}]: {chunk['content']}")
    context = "\n\n".join(context_parts) if context_parts else "(No documents found)"
    return PROMPT_TEMPLATE.format(context=context, question=question)


class RetrieverService:
    def __init__(self, repo: "VectorStoreRepository", llm: LLMService, top_k: int):
        self._repo = repo
        self._llm = llm
        self._top_k = top_k

    def query(
        self, question: str, document_ids: list[str] | None = None
    ) -> tuple[Iterator[str], list[dict]]:
        chunks = self._repo.search(question, top_k=self._top_k, document_ids=document_ids)
        prompt = build_prompt(chunks, question)
        token_stream = self._llm.generate_stream(prompt)
        sources = [
            {"document": c["document"], "excerpt": c["content"][:200]}
            for c in chunks
        ]
        return token_stream, sources

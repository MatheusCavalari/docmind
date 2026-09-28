import io
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

from app.models.schemas import DocumentResponse

if TYPE_CHECKING:
    from app.repositories.vector_store import VectorStoreRepository


class IngestService:
    SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}

    def __init__(self, repo: "VectorStoreRepository", chunk_size: int, chunk_overlap: int):
        self._repo = repo
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def ingest(self, file_content: bytes, filename: str) -> DocumentResponse:
        ext = self._get_extension(filename)
        if ext not in self.SUPPORTED_EXTENSIONS:
            supported = ', '.join(self.SUPPORTED_EXTENSIONS)
            raise ValueError(f"Unsupported file type: {ext}. Supported: {supported}")

        text = self._parse(file_content, ext)
        if not text.strip():
            raise ValueError("No text content found in the uploaded file.")

        chunks = self._splitter.split_text(text)
        if not chunks:
            raise ValueError("No text content found in the uploaded file.")

        doc_id = str(uuid.uuid4())
        chunk_count = self._repo.add_document(doc_id, chunks, filename)

        return DocumentResponse(
            id=doc_id,
            filename=filename,
            chunks=chunk_count,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    def _parse(self, content: bytes, ext: str) -> str:
        if ext == ".pdf":
            return self._parse_pdf(content)
        return content.decode("utf-8", errors="replace")

    def _parse_pdf(self, content: bytes) -> str:
        reader = PdfReader(io.BytesIO(content))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
        return "\n\n".join(pages)

    def _get_extension(self, filename: str) -> str:
        dot_idx = filename.rfind(".")
        if dot_idx == -1:
            return ""
        return filename[dot_idx:].lower()

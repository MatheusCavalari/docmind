import pytest
from unittest.mock import MagicMock
from app.services.ingest import IngestService


@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.add_document.return_value = 3
    return repo


@pytest.fixture
def service(mock_repo):
    return IngestService(repo=mock_repo, chunk_size=100, chunk_overlap=20)


def test_ingest_txt_file(service, mock_repo):
    content = b"This is a simple text file with some content for testing."
    result = service.ingest(content, "test.txt")
    assert result.filename == "test.txt"
    assert result.chunks == 3
    assert result.id is not None
    mock_repo.add_document.assert_called_once()


def test_ingest_md_file(service, mock_repo):
    content = b"# Heading\n\nSome markdown content here."
    result = service.ingest(content, "readme.md")
    assert result.filename == "readme.md"
    mock_repo.add_document.assert_called_once()


def test_ingest_pdf_file(service, mock_repo):
    # Create a minimal valid PDF
    from PyPDF2 import PdfWriter
    import io
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    page = writer.pages[0]
    # We'll test with a real PDF that has no text — should raise ValueError
    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()
    with pytest.raises(ValueError, match="No text content"):
        service.ingest(pdf_bytes, "empty.pdf")


def test_ingest_unsupported_format(service):
    with pytest.raises(ValueError, match="Unsupported file type"):
        service.ingest(b"data", "image.png")


def test_ingest_empty_file(service):
    with pytest.raises(ValueError, match="No text content"):
        service.ingest(b"", "empty.txt")


def test_chunk_splitting(mock_repo):
    mock_repo.add_document.return_value = 0
    service = IngestService(repo=mock_repo, chunk_size=50, chunk_overlap=10)
    text = "A" * 200
    mock_repo.add_document.side_effect = lambda doc_id, chunks, filename: len(chunks)
    result = service.ingest(text.encode(), "long.txt")
    assert result.chunks > 1

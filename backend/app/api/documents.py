from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import DocumentResponse

router = APIRouter(prefix="/api")


def get_ingest_service():
    from app.main import _ingest_service
    return _ingest_service


def get_vector_store():
    from app.main import _vector_store
    return _vector_store


@router.post("/documents", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()
    if len(content) > 10_485_760:
        raise HTTPException(status_code=400, detail="File too large. Max 10MB.")
    try:
        result = get_ingest_service().ingest(content, file.filename or "unknown")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.get("/documents", response_model=list[DocumentResponse])
async def list_documents():
    store = get_vector_store()
    doc_ids = store.list_document_ids()
    docs = []
    for doc_id in doc_ids:
        all_meta = store._collection.get(where={"doc_id": doc_id}, include=["metadatas"])
        if all_meta["metadatas"]:
            filename = all_meta["metadatas"][0]["document"]
            chunk_count = len(all_meta["metadatas"])
            docs.append(DocumentResponse(
                id=doc_id,
                filename=filename,
                chunks=chunk_count,
                created_at="",
            ))
    return docs


@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(doc_id: str):
    get_vector_store().delete_document(doc_id)

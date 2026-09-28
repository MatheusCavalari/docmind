import chromadb
from langchain_huggingface import HuggingFaceEmbeddings


class VectorStoreRepository:
    def __init__(self, persist_dir: str, embedding_model: str):
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self._collection = self._client.get_or_create_collection(
            name="docmind",
            metadata={"hnsw:space": "cosine"},
        )

    def add_document(self, doc_id: str, chunks: list[str], filename: str) -> int:
        if not chunks:
            return 0
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        embeddings = self._embeddings.embed_documents(chunks)
        metadatas = [
            {"doc_id": doc_id, "document": filename, "chunk_index": i}
            for i in range(len(chunks))
        ]
        self._collection.add(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )
        return len(chunks)

    def delete_document(self, doc_id: str) -> None:
        self._collection.delete(where={"doc_id": doc_id})

    def search(
        self, query: str, top_k: int = 4, document_ids: list[str] | None = None
    ) -> list[dict]:
        query_embedding = self._embeddings.embed_query(query)
        where_filter = None
        if document_ids:
            if len(document_ids) == 1:
                where_filter = {"doc_id": document_ids[0]}
            else:
                where_filter = {"doc_id": {"$in": document_ids}}
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
        )
        output = []
        if results["documents"] and results["metadatas"]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                output.append({
                    "content": doc,
                    "document": meta["document"],
                    "chunk_index": meta["chunk_index"],
                })
        return output

    def count_documents(self) -> int:
        all_meta = self._collection.get(include=["metadatas"])
        doc_ids = set()
        if all_meta["metadatas"]:
            for meta in all_meta["metadatas"]:
                doc_ids.add(meta["doc_id"])
        return len(doc_ids)

    def list_document_ids(self) -> list[str]:
        all_meta = self._collection.get(include=["metadatas"])
        doc_ids = set()
        if all_meta["metadatas"]:
            for meta in all_meta["metadatas"]:
                doc_ids.add(meta["doc_id"])
        return list(doc_ids)

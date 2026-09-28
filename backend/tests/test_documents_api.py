import io


def test_upload_txt_document(client):
    file = io.BytesIO(b"This is a test document with enough content to be meaningful.")
    response = client.post(
        "/api/documents",
        files={"file": ("test.txt", file, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["chunks"] >= 1
    assert "id" in data
    assert "created_at" in data


def test_upload_unsupported_format(client):
    file = io.BytesIO(b"data")
    response = client.post(
        "/api/documents",
        files={"file": ("image.png", file, "image/png")},
    )
    assert response.status_code == 400


def test_list_documents_empty(client):
    response = client.get("/api/documents")
    assert response.status_code == 200
    assert response.json() == []


def test_list_documents_after_upload(client):
    file = io.BytesIO(b"Test content for listing documents after upload flow.")
    client.post("/api/documents", files={"file": ("a.txt", file, "text/plain")})
    response = client.get("/api/documents")
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "a.txt"


def test_delete_document(client):
    file = io.BytesIO(b"Content to be deleted in this test flow.")
    upload = client.post("/api/documents", files={"file": ("del.txt", file, "text/plain")})
    doc_id = upload.json()["id"]
    response = client.delete(f"/api/documents/{doc_id}")
    assert response.status_code == 204
    listing = client.get("/api/documents")
    assert len(listing.json()) == 0


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model" in data
    assert "documents_count" in data

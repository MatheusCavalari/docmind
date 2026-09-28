<div align="center">

# DocMind

**Retrieval-Augmented Generation Document Assistant**

[![CI](https://github.com/MatheusCavalari/docmind/actions/workflows/ci.yml/badge.svg)](https://github.com/MatheusCavalari/docmind/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18-61dafb?logo=react&logoColor=white)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Upload documents. Ask questions. Get grounded answers with source citations — powered entirely by open-source models on a free-tier infrastructure.

[Getting Started](#getting-started) · [Architecture](#architecture) · [API Reference](#api-reference) · [Development](#development)

</div>

---

## Overview

DocMind is a full-stack RAG (Retrieval-Augmented Generation) application that enables conversational interaction with uploaded documents. It combines local semantic embeddings with LLM-powered generation to deliver accurate, citation-backed answers — all running on a zero-cost stack.

### Key Capabilities

- **Multi-format ingestion** — PDF, Markdown, and plain text (up to 10 MB per file)
- **Semantic retrieval** — vector similarity search over document chunks using local embeddings
- **Grounded generation** — answers strictly based on retrieved context, with source excerpts
- **Real-time streaming** — token-by-token response delivery via Server-Sent Events (SSE)
- **One-command deployment** — fully containerized with Docker Compose

## Architecture

```
                         ┌─────────────────────────────────────────────┐
                         │              FastAPI Backend                │
┌──────────────┐         │                                             │
│              │  HTTP   │  /api/documents   Upload · List · Delete    │
│  React SPA   │────────▶│  /api/chat        SSE streaming responses  │
│  Vite + TS   │◀────────│  /api/health      Readiness probe          │
│  Tailwind    │   SSE   │                                             │
│              │         │  ┌──────────────┐  ┌─────────────────────┐  │
└──────────────┘         │  │  LangChain   │  │     ChromaDB        │  │
   Port 3000             │  │  + HF Inf.   │  │  (vector store)     │  │
                         │  │  API (free)  │  │  local, embedded    │  │
                         │  └──────────────┘  └─────────────────────┘  │
                         │              Port 8000                      │
                         └─────────────────────────────────────────────┘
```

### RAG Pipeline

**Ingestion** — Document → text extraction → recursive chunking (1000 chars, 200 overlap) → embedding via `all-MiniLM-L6-v2` (local, CPU-only) → persisted in ChromaDB.

**Query** — Question → embedding → top-4 similarity search → prompt construction with retrieved context → Mistral-7B generation via HuggingFace Inference API → streamed response with source citations.

## Tech Stack

| Layer | Technology | Details |
|-------|------------|---------|
| **Backend** | Python 3.12 · FastAPI · LangChain | Layered architecture: `api/` → `services/` → `repositories/` |
| **LLM** | Mistral-7B-Instruct v0.3 | HuggingFace Inference API — free tier, no GPU required |
| **Embeddings** | sentence-transformers | `all-MiniLM-L6-v2` — ~80 MB model, runs locally on CPU |
| **Vector Store** | ChromaDB | Embedded mode, persistent storage, HNSW indexing |
| **Frontend** | React 18 · TypeScript · Vite | Tailwind CSS dark theme, custom hooks for state management |
| **Infrastructure** | Docker Compose | 2-service stack: backend (:8000) + frontend/nginx (:3000) |
| **CI** | GitHub Actions | Ruff linting, pytest, Docker Compose build verification |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2+
- A free [HuggingFace](https://huggingface.co/join) API token

### Quick Start

```bash
git clone https://github.com/MatheusCavalari/docmind.git
cd docmind
cp .env.example .env    # add your HF token to .env
docker compose up --build
```

Open **http://localhost:3000** — upload a document and start chatting.

## Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Testing

```bash
# Backend tests
cd backend
ruff check .
pytest -v

# Frontend lint + type check
cd frontend
npm run lint
npm run build
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents` | Upload a document (`multipart/form-data`) |
| `GET` | `/api/documents` | List all indexed documents |
| `DELETE` | `/api/documents/{id}` | Remove a document and its vectors |
| `POST` | `/api/chat` | Chat with documents — returns an SSE stream |
| `GET` | `/api/health` | Health check (status, model info, document count) |

### Chat Request

```json
{
  "question": "What are the main findings?",
  "document_ids": ["optional-filter-by-doc-id"]
}
```

### SSE Event Types

| Event | Payload | Description |
|-------|---------|-------------|
| `token` | `{ "token": "..." }` | Incremental text token |
| `sources` | `{ "sources": [...] }` | Array of `{ document, excerpt }` citations |
| `error` | `{ "message": "..." }` | Error details |

## Project Structure

```
docmind/
├── backend/
│   ├── app/
│   │   ├── api/            # Route handlers (documents, chat, health)
│   │   ├── services/       # Business logic (ingest, retriever, LLM)
│   │   ├── repositories/   # Data layer (ChromaDB vector store)
│   │   └── models/         # Pydantic request/response schemas
│   ├── tests/              # pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/     # UI components (ChatPanel, DocumentList, ...)
│   │   └── hooks/          # Custom hooks (useDocuments, useChat)
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .github/workflows/ci.yml
└── .env.example
```

## License

This project is licensed under the [MIT License](LICENSE).

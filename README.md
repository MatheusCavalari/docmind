# DocMind

A RAG (Retrieval-Augmented Generation) document assistant that lets you upload documents and chat with them using AI. Built with FastAPI, React, and LangChain — 100% free to run using HuggingFace's open-source models.

## Features

- **Document Upload** — Upload PDF, Markdown, or TXT files (up to 10MB)
- **AI-Powered Chat** — Ask questions about your documents in natural language
- **Source Citations** — Every answer includes the document excerpts it was based on
- **Streaming Responses** — Real-time token-by-token responses via Server-Sent Events
- **Docker Ready** — Single `docker compose up` to run everything

## Architecture

```
┌─────────────┐     ┌──────────────────────────────────┐
│  React SPA  │────▶│  FastAPI Backend                  │
│  (Vite+TS)  │     │                                   │
│             │     │  POST /api/documents  (upload)     │
│  - Upload   │     │  POST /api/chat       (query)      │
│  - Chat UI  │     │  GET  /api/documents  (list)       │
│  - Sources  │     │  DELETE /api/documents/:id         │
└─────────────┘     │                                   │
                    │  ┌─────────────┐ ┌──────────────┐ │
                    │  │ LangChain   │ │ ChromaDB     │ │
                    │  │ + HF Inf.   │ │ (vectors)    │ │
                    │  └─────────────┘ └──────────────┘ │
                    └──────────────────────────────────┘
```

## RAG Pipeline

### Ingestion

1. User uploads a document (PDF, Markdown, or TXT)
2. Text is extracted and split into overlapping chunks (1000 chars, 200 overlap)
3. Each chunk is embedded using `all-MiniLM-L6-v2` (runs locally, no API needed)
4. Chunks + embeddings are stored in ChromaDB

### Query

1. User asks a question
2. The question is embedded and matched against stored chunks (top 4)
3. A prompt is constructed with the relevant chunks as context
4. Mistral-7B generates a grounded answer via HuggingFace Inference API
5. The response is streamed back with source citations

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI, LangChain |
| LLM | Mistral-7B-Instruct via HuggingFace (free tier) |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` (local) |
| Vector Store | ChromaDB (embedded) |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Infrastructure | Docker Compose |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- A free [HuggingFace account](https://huggingface.co/join) and API token

### Setup

1. Clone the repository:

```bash
git clone https://github.com/MatheusCavalari/docmind.git
cd docmind
```

2. Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your HuggingFace API token
```

3. Run with Docker:

```bash
docker compose up --build
```

4. Open http://localhost:3000 in your browser

### Development (without Docker)

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/documents` | Upload a document (multipart/form-data) |
| `GET` | `/api/documents` | List all documents |
| `DELETE` | `/api/documents/{id}` | Delete a document |
| `POST` | `/api/chat` | Chat with documents (SSE stream) |
| `GET` | `/api/health` | Health check |

## Project Structure

```
docmind/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes
│   │   ├── services/     # Business logic (ingest, retriever, LLM)
│   │   ├── repositories/ # Data access (ChromaDB)
│   │   └── models/       # Pydantic schemas
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   └── hooks/        # Custom hooks (useDocuments, useChat)
│   └── ...
├── docker-compose.yml
└── README.md
```

## License

MIT

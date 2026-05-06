# ContextLayer — Legal RAG Demo

## Project Purpose

Build a fully containerised RAG (Retrieval-Augmented Generation) system that lets users ask questions against a set of legal documents and get accurate answers with source citations. Everything runs locally inside Docker — no external APIs, no data leaving the machine.

This is a portfolio demo targeting law firms and professional services clients. The key selling points are:
- One command to run (`docker-compose up`)
- Fully private — no data sent to any external provider
- Source citations on every answer — users can download and verify the source document
- Production-credible stack that mirrors real client deployments

---

## Stack

| Layer | Tool | Notes |
|---|---|---|
| LLM | Ollama + Llama 3.1 8B | Runs inside Docker container |
| Vector DB | Qdrant | Runs inside Docker container |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 | Runs in app container, no API needed |
| RAG Framework | LlamaIndex | Primary framework — use this, not LangChain |
| Frontend | Streamlit | Two-column layout — chat left, document library right |
| Orchestration | Docker Compose | Three containers: ollama, qdrant, app |

---

## Repo Structure

Build exactly this structure — do not deviate:

```
contextlayer-legal-rag/
├── docker-compose.yml
├── Dockerfile
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── CLAUDE.md
├── README.md
├── rag/
│   ├── __init__.py
│   ├── ingest.py
│   ├── retriever.py
│   ├── generator.py
│   └── prompts.py
└── docs/
    ├── nda-template.pdf
    ├── service-agreement.pdf
    ├── employment-contract.pdf
    ├── ip-assignment.pdf
    └── privacy-policy.pdf
```

---

## config.py

All constants live here. No magic numbers anywhere else in the codebase.

```python
# Qdrant
QDRANT_HOST = "qdrant"          # Docker service name
QDRANT_PORT = 6333
QDRANT_COLLECTION = "legal-docs"

# Ollama
OLLAMA_HOST = "ollama"          # Docker service name
OLLAMA_PORT = 11434
OLLAMA_MODEL = "llama3.1:8b"

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384

# Chunking
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

# Retrieval
TOP_K = 5

# Demo limits
MAX_QUERIES_PER_SESSION = 10

# Branding
DEMO_NAME = "Legal Document Q&A"
DEMO_VERTICAL = "Legal"
ACCENT_COLOR = "#4f8ef7"
```

---

## docker-compose.yml

Three services. App depends on both ollama and qdrant being healthy before starting.

```yaml
version: "3.9"

services:
  ollama:
    image: ollama/ollama
    container_name: contextlayer_ollama
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434"]
      interval: 10s
      timeout: 5s
      retries: 5

  qdrant:
    image: qdrant/qdrant
    container_name: contextlayer_qdrant
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/healthz"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    container_name: contextlayer_app
    ports:
      - "8501:8501"
    depends_on:
      ollama:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    volumes:
      - ./docs:/app/docs
    environment:
      - QDRANT_HOST=qdrant
      - OLLAMA_HOST=ollama

volumes:
  ollama_data:
  qdrant_data:
```

---

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pull the embedding model at build time so it's cached in the image
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
```

---

## requirements.txt

Pin these exact packages:

```
streamlit>=1.32.0
llama-index>=0.10.0
llama-index-vector-stores-qdrant>=0.2.0
llama-index-embeddings-huggingface>=0.2.0
llama-index-llms-ollama>=0.1.0
qdrant-client>=1.8.0
sentence-transformers>=2.6.0
python-dotenv>=1.0.0
```

---

## rag/ingest.py

This script is run once to load documents into Qdrant. It must be runnable both locally (for development) and inside the app container on first startup.

Requirements:
- Use LlamaIndex `SimpleDirectoryReader` to load all PDFs from the `/docs` folder
- Use LlamaIndex `SentenceSplitter` with `CHUNK_SIZE` and `CHUNK_OVERLAP` from config
- Embed chunks using `HuggingFaceEmbedding` with `EMBEDDING_MODEL` from config
- Store each chunk in Qdrant with metadata: `source_file` (filename only, not full path), `page_number`, `chunk_index`
- Check if collection already exists before creating — do not re-ingest if collection already has points
- Print progress: document count loaded, chunk count created, confirmation when pushed to Qdrant
- Handle connection errors to Qdrant and Ollama with clear error messages

---

## rag/retriever.py

Requirements:
- Function signature: `retrieve(query: str, top_k: int = TOP_K) -> list[dict]`
- Embed the query using the same `all-MiniLM-L6-v2` model used during ingest
- Query Qdrant collection for top K results
- Return a list of dicts, each containing:
  - `text`: the chunk text
  - `source_file`: filename (e.g. `nda-template.pdf`)
  - `page_number`: page number as integer, None if unavailable
  - `score`: similarity score as float
- Handle Qdrant connection errors gracefully

---

## rag/prompts.py

Two prompt templates:

**System prompt requirements:**
- Instruct the model to answer ONLY from the provided document context
- Instruct the model to cite the source filename for every claim it makes
- Instruct the model to say exactly "I cannot find this information in the provided documents." if the answer is not in the context
- Do not instruct the model to make up or infer answers beyond what is in the documents
- Keep it concise — under 150 words

**User prompt template requirements:**
- Accepts `context_chunks` (list of chunk texts with their source filenames) and `question`
- Formats context clearly with source labels before each chunk
- Asks the question at the end
- Example format:
```
Context:
[Source: nda-template.pdf]
...chunk text...

[Source: service-agreement.pdf]
...chunk text...

Question: {question}
```

---

## rag/generator.py

Requirements:
- Function signature: `generate(query: str, chunks: list[dict]) -> str`
- Build the prompt using `prompts.py` templates
- Call Ollama via LlamaIndex `Ollama` LLM class using `OLLAMA_MODEL` and `OLLAMA_HOST` from config
- Use streaming — yield tokens as they arrive for display in Streamlit
- Handle Ollama connection errors with a clear user-facing error message
- Do not add any content beyond what the model returns — no post-processing of the answer

---

## app.py

### Layout

Two-column Streamlit layout:
- Left column (ratio 2): chat interface
- Right column (ratio 1): document library + session counter

### Header

```
ContextLayer  /  Legal Document Q&A
```

Tagline below: *"Ask questions against the knowledge base. Every answer includes a source citation you can verify."*

### Left column — chat interface

- `st.chat_input` for question entry
- Display full conversation history from `st.session_state.messages`
- On each new question:
  1. Add user message to history
  2. Call `retriever.retrieve(query)`
  3. Call `generator.generate(query, chunks)` with streaming
  4. Display streamed answer using `st.write_stream`
  5. Below the answer, display citations panel (see below)
  6. Add assistant message + citations to history
  7. Decrement query counter

- When query counter hits 0: disable input, show message "Demo query limit reached. Contact ContextLayer to discuss your use case."

### Citations panel

Displayed below each answer, inside an `st.expander` labelled "Sources (N documents)":

For each unique source document cited:
- Document name as a label
- Excerpt of the relevant chunk (first 200 chars)
- Page number if available
- `st.download_button` that reads the file from `/app/docs/` and serves it as a PDF download

### Right column — document library

Section header: "KNOWLEDGE BASE"

List every PDF in the `/app/docs/` folder:
- Document name (filename without extension, title-cased)
- `st.download_button` for each file
- Small descriptive label per document (hardcode these based on the actual files)

Section header below: "SESSION"

Display: "X of 10 queries remaining" where X decrements with each query.

Show a simple progress bar using `st.progress`.

### Session state keys

Initialise these on app load:
- `messages`: list of conversation history
- `query_count`: integer starting at 0
- `ingestion_complete`: boolean

### Ingestion on startup

On first load, check if Qdrant collection exists and has points. If not, run ingestion automatically with a spinner: "Loading knowledge base..." Do not show the chat interface until ingestion is complete.

### Styling

Apply this CSS via `st.markdown`:
- Background: `#0d1117`
- Font: DM Mono (import from Google Fonts)
- Accent: `#4f8ef7`
- Text: `#c9d1d9`
- Border colour: `#1a2535`
- Chat message background: `#0f1923`

---

## Synthetic Documents

The `/docs` folder must contain five PDF files. Create realistic but clearly fictional legal documents. Use the fictional company name "Meridian Group Ltd" as the client and "Vantage Legal LLP" as the law firm throughout all documents for consistency.

| File | Content |
|---|---|
| `nda-template.pdf` | 2-page mutual NDA. Covers definition of confidential information, obligations, exclusions, term (2 years), governing law (Delaware). |
| `service-agreement.pdf` | 3-page professional services agreement. Covers scope of work, payment terms (net-30), IP ownership, limitation of liability, termination clauses. |
| `employment-contract.pdf` | 3-page employment contract. Covers role and responsibilities, compensation, benefits, non-compete (12 months, 50-mile radius), termination notice periods. |
| `ip-assignment.pdf` | 2-page IP assignment agreement. Covers assignment of work product, moral rights waiver, prior inventions carve-out, consideration. |
| `privacy-policy.pdf` | 2-page internal privacy policy. Covers data collected, retention periods, third-party sharing, employee rights, GDPR compliance statement. |

Write these documents with enough specific detail that a user asking realistic legal questions will get useful cited answers. Include specific clause numbers, defined terms, and realistic legal language throughout.

---

## README.md

Write a README that sells the project to a technical buyer, not just documents it.

Structure:
1. Project title and one-line description
2. Live demo GIF placeholder (add placeholder text: `[Demo GIF — coming soon]`)
3. One-command setup section — this must be the third thing on the page
4. What this does — 3 bullet points on the business problem
5. Architecture section — simple ASCII diagram of the three containers
6. Stack table
7. Full setup instructions
8. How to add your own documents
9. Deployment note — explain this runs fully locally, no data leaves the machine
10. Built by ContextLayer footer

The one-command setup block must look exactly like this:

```bash
git clone https://github.com/yourusername/contextlayer-legal-rag
cd contextlayer-legal-rag
docker-compose up
# Open http://localhost:8501
```

---

## Build Order

Execute in this exact order. Do not move to the next step until the current step is verified working.

1. Create repo structure and all empty files
2. Write `config.py`
3. Write `docker-compose.yml` and `Dockerfile`
4. Write `requirements.txt`
5. Write synthetic legal documents and save as PDFs to `/docs`
6. Write `rag/prompts.py`
7. Write `rag/ingest.py` — test locally against docs folder
8. Write `rag/retriever.py` — test with 5 sample questions
9. Write `rag/generator.py` — test end-to-end pipeline from command line
10. Write `app.py` — wire everything together
11. Run `docker-compose up` — verify full stack works
12. Write `README.md`

---

## Coding Conventions

- Python 3.11
- Type hints on all function signatures
- Docstrings on all functions — one line describing what it does
- No print statements in production code — use `logging` with appropriate levels
- All configuration from `config.py` — no hardcoded values in other files
- All file paths use `pathlib.Path` — no string concatenation for paths
- Error handling: catch specific exceptions, not bare `except:`
- Never commit secrets — `.env.example` with placeholder values only

---

## What Not to Change

- The three-container Docker Compose architecture — do not collapse into fewer containers
- LlamaIndex as the RAG framework — do not substitute LangChain
- The `source_file` and `page_number` metadata fields — citations depend on these
- The `MAX_QUERIES_PER_SESSION` limit — this must be enforced in the UI
- The two-column Streamlit layout — chat left, library right


## First Task

Before writing any code, create a file called `TODO.md` in the repo root.
Generate a detailed task checklist based on the Build Order section of this
document. Break each step into granular subtasks. Use GitHub checkbox format.
Update TODO.md as tasks are completed — check off each item before moving
to the next step.

## Git Workflow

- Work on a feature branch per session — never commit directly to main
- Branch naming: `session-[N]-[task]` e.g. `session-3-ingest`
- Commit messages must describe what was built and verified, not just "update files"
- Push the branch at the end of each session
- Do not merge to main — that is done manually after review
- Never commit: `.env`, `__pycache__`, `.DS_Store`, model weights, or any file 
  over 50MB
- The `/docs` PDFs are committed — they are demo assets, not sensitive data


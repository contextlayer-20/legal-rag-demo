# ContextLayer Legal RAG Demo — Task Checklist

## Step 1 — Repo Structure
- [x] Create feature branch (`session-1-scaffold`)
- [x] Create `TODO.md`
- [x] Create all empty files and directories per the spec
  - [x] `rag/__init__.py`
  - [x] `rag/ingest.py`
  - [x] `rag/retriever.py`
  - [x] `rag/generator.py`
  - [x] `rag/prompts.py`
  - [x] `docs/` directory
  - [x] `app.py`
  - [x] `config.py`
  - [x] `requirements.txt`
  - [x] `docker-compose.yml`
  - [x] `Dockerfile`
  - [x] `.env.example`
  - [x] `.gitignore`
  - [x] `README.md`

## Step 2 — config.py
- [x] Write all constants (Qdrant, Ollama, Embeddings, Chunking, Retrieval, Demo limits, Branding)
- [x] Verify no magic numbers exist anywhere else

## Step 3 — docker-compose.yml and Dockerfile
- [x] Write `docker-compose.yml` with three services (ollama, qdrant, app)
- [x] Add healthchecks for ollama and qdrant
- [x] Add `depends_on` with health conditions for app
- [x] Write `Dockerfile` (python:3.11-slim, pre-cache embedding model)

## Step 4 — requirements.txt
- [x] Pin all packages per spec
  - [x] `streamlit>=1.32.0`
  - [x] `llama-index>=0.10.0`
  - [x] `llama-index-vector-stores-qdrant>=0.2.0`
  - [x] `llama-index-embeddings-huggingface>=0.2.0`
  - [x] `llama-index-llms-ollama>=0.1.0`
  - [x] `qdrant-client>=1.8.0`
  - [x] `sentence-transformers>=2.6.0`
  - [x] `python-dotenv>=1.0.0`

## Step 5 — Synthetic Legal Documents
- [x] Write `docs/nda-template.pdf` (2-page mutual NDA)
- [x] Write `docs/service-agreement.pdf` (3-page professional services agreement)
- [x] Write `docs/employment-contract.pdf` (3-page employment contract)
- [x] Write `docs/ip-assignment.pdf` (2-page IP assignment)
- [x] Write `docs/privacy-policy.pdf` (2-page internal privacy policy)
- [x] Verify all docs use Meridian Group Ltd / Vantage Legal LLP consistently
- [x] Verify specific clause numbers and defined terms in each doc

## Step 6 — rag/prompts.py
- [x] Write system prompt (answer only from context, cite sources, fallback phrase)
- [x] Write user prompt template (context_chunks + question)
- [x] Verify system prompt is under 150 words

## Step 7 — scripts/ingest.py
- [x] Load PDFs with `SimpleDirectoryReader`
- [x] Chunk with `SentenceSplitter` using config values
- [x] Embed with `HuggingFaceEmbedding`
- [x] Store in Qdrant with `source_file`, `page_number`, `chunk_index` metadata
- [x] Check for existing collection before ingesting
- [x] Add progress logging
- [x] Add connection error handling
- [x] Test locally against docs folder

## Step 8 — rag/retriever.py
- [x] Implement `retrieve(query, top_k)` function signature
- [x] Embed query with same model as ingest
- [x] Query Qdrant for top K results
- [x] Return list of dicts with `text`, `source_file`, `page_number`, `score`
- [x] Handle Qdrant connection errors
- [x] Test with 5 sample questions

## Step 9 — rag/generator.py
- [x] Implement `generate(query, chunks)` function signature
- [x] Build prompt using prompts.py templates
- [x] Call Ollama via LlamaIndex `Ollama` class
- [x] Implement streaming (yield tokens)
- [x] Handle Ollama connection errors
- [x] Test end-to-end pipeline from command line

## Step 10 — app.py
- [x] Two-column layout (ratio 2:1)
- [x] Header: "ContextLayer / Legal Document Q&A" + tagline
- [x] Left column: chat interface with `st.chat_input`
- [x] Display full conversation history from session state
- [x] On query: retrieve → generate (streaming) → display citations
- [x] Citations panel in `st.expander` with download buttons
- [x] Query limit enforcement (disable input at 0)
- [x] Right column: document library with download buttons
- [x] Right column: session counter + progress bar
- [x] Ingestion on startup with spinner
- [x] Apply custom CSS (dark theme, DM Mono font)
- [x] Initialise all session state keys

## Step 11 — Docker Compose Full Stack
- [x] Run `docker-compose up`
- [x] Verify ollama container starts and is healthy
- [x] Verify qdrant container starts and is healthy
- [x] Verify app container builds and starts
- [x] Verify ingestion runs on first startup
- [x] Test 3+ questions end-to-end with citations
- [x] Verify download buttons work

## Step 12 — README.md
- [x] Project title and one-line description
- [x] Demo GIF placeholder
- [x] One-command setup block (exact format per spec)
- [x] "What this does" — 3 bullet points
- [x] Architecture ASCII diagram
- [x] Stack table
- [x] Full setup instructions
- [x] How to add your own documents
- [x] Deployment/privacy note
- [x] ContextLayer footer

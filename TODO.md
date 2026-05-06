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
- [ ] Write system prompt (answer only from context, cite sources, fallback phrase)
- [ ] Write user prompt template (context_chunks + question)
- [ ] Verify system prompt is under 150 words

## Step 7 — scripts/ingest.py
- [ ] Load PDFs with `SimpleDirectoryReader`
- [ ] Chunk with `SentenceSplitter` using config values
- [ ] Embed with `HuggingFaceEmbedding`
- [ ] Store in Qdrant with `source_file`, `page_number`, `chunk_index` metadata
- [ ] Check for existing collection before ingesting
- [ ] Add progress logging
- [ ] Add connection error handling
- [ ] Test locally against docs folder

## Step 8 — rag/retriever.py
- [ ] Implement `retrieve(query, top_k)` function signature
- [ ] Embed query with same model as ingest
- [ ] Query Qdrant for top K results
- [ ] Return list of dicts with `text`, `source_file`, `page_number`, `score`
- [ ] Handle Qdrant connection errors
- [ ] Test with 5 sample questions

## Step 9 — rag/generator.py
- [ ] Implement `generate(query, chunks)` function signature
- [ ] Build prompt using prompts.py templates
- [ ] Call Ollama via LlamaIndex `Ollama` class
- [ ] Implement streaming (yield tokens)
- [ ] Handle Ollama connection errors
- [ ] Test end-to-end pipeline from command line

## Step 10 — app.py
- [ ] Two-column layout (ratio 2:1)
- [ ] Header: "ContextLayer / Legal Document Q&A" + tagline
- [ ] Left column: chat interface with `st.chat_input`
- [ ] Display full conversation history from session state
- [ ] On query: retrieve → generate (streaming) → display citations
- [ ] Citations panel in `st.expander` with download buttons
- [ ] Query limit enforcement (disable input at 0)
- [ ] Right column: document library with download buttons
- [ ] Right column: session counter + progress bar
- [ ] Ingestion on startup with spinner
- [ ] Apply custom CSS (dark theme, DM Mono font)
- [ ] Initialise all session state keys

## Step 11 — Docker Compose Full Stack
- [ ] Run `docker-compose up`
- [ ] Verify ollama container starts and is healthy
- [ ] Verify qdrant container starts and is healthy
- [ ] Verify app container builds and starts
- [ ] Verify ingestion runs on first startup
- [ ] Test 3+ questions end-to-end with citations
- [ ] Verify download buttons work

## Step 12 — README.md
- [ ] Project title and one-line description
- [ ] Demo GIF placeholder
- [ ] One-command setup block (exact format per spec)
- [ ] "What this does" — 3 bullet points
- [ ] Architecture ASCII diagram
- [ ] Stack table
- [ ] Full setup instructions
- [ ] How to add your own documents
- [ ] Deployment/privacy note
- [ ] ContextLayer footer

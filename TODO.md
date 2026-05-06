# ContextLayer Legal RAG Demo — Task Checklist

## Step 1 — Repo Structure
- [x] Create feature branch (`session-1-scaffold`)
- [x] Create `TODO.md`
- [ ] Create all empty files and directories per the spec
  - [ ] `rag/__init__.py`
  - [ ] `rag/ingest.py`
  - [ ] `rag/retriever.py`
  - [ ] `rag/generator.py`
  - [ ] `rag/prompts.py`
  - [ ] `docs/` directory
  - [ ] `app.py`
  - [ ] `config.py`
  - [ ] `requirements.txt`
  - [ ] `docker-compose.yml`
  - [ ] `Dockerfile`
  - [ ] `.env.example`
  - [ ] `.gitignore`
  - [ ] `README.md`

## Step 2 — config.py
- [ ] Write all constants (Qdrant, Ollama, Embeddings, Chunking, Retrieval, Demo limits, Branding)
- [ ] Verify no magic numbers exist anywhere else

## Step 3 — docker-compose.yml and Dockerfile
- [ ] Write `docker-compose.yml` with three services (ollama, qdrant, app)
- [ ] Add healthchecks for ollama and qdrant
- [ ] Add `depends_on` with health conditions for app
- [ ] Write `Dockerfile` (python:3.11-slim, pre-cache embedding model)

## Step 4 — requirements.txt
- [ ] Pin all packages per spec
  - [ ] `streamlit>=1.32.0`
  - [ ] `llama-index>=0.10.0`
  - [ ] `llama-index-vector-stores-qdrant>=0.2.0`
  - [ ] `llama-index-embeddings-huggingface>=0.2.0`
  - [ ] `llama-index-llms-ollama>=0.1.0`
  - [ ] `qdrant-client>=1.8.0`
  - [ ] `sentence-transformers>=2.6.0`
  - [ ] `python-dotenv>=1.0.0`

## Step 5 — Synthetic Legal Documents
- [ ] Write `docs/nda-template.pdf` (2-page mutual NDA)
- [ ] Write `docs/service-agreement.pdf` (3-page professional services agreement)
- [ ] Write `docs/employment-contract.pdf` (3-page employment contract)
- [ ] Write `docs/ip-assignment.pdf` (2-page IP assignment)
- [ ] Write `docs/privacy-policy.pdf` (2-page internal privacy policy)
- [ ] Verify all docs use Meridian Group Ltd / Vantage Legal LLP consistently
- [ ] Verify specific clause numbers and defined terms in each doc

## Step 6 — rag/prompts.py
- [ ] Write system prompt (answer only from context, cite sources, fallback phrase)
- [ ] Write user prompt template (context_chunks + question)
- [ ] Verify system prompt is under 150 words

## Step 7 — rag/ingest.py
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

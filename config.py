import os

# Qdrant
QDRANT_HOST = os.environ.get("QDRANT_HOST", "qdrant")   # Docker service name; override for local dev
QDRANT_PORT = 6333
QDRANT_COLLECTION = "legal-docs"

# Ollama
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "ollama")   # Docker service name; override for local dev
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
MAX_QUERIES_PER_SESSION = 0     # 0 = no limit (local/GitHub demo)
                                # Set to 10 for hosted/public demo

# Branding
DEMO_NAME = "Legal Document Q&A"
DEMO_VERTICAL = "Legal"
ACCENT_COLOR = "#4f8ef7"

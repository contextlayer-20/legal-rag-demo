"""Streaming answer generator for the legal RAG pipeline."""

import logging
from collections.abc import Generator

from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.ollama import Ollama

from config import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_PORT
from rag.prompts import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger(__name__)


def generate(query: str, chunks: list[dict]) -> Generator[str, None, None]:
    """Stream answer tokens from Ollama given a query and retrieved chunks."""
    user_prompt = build_user_prompt(chunks, query)
    messages = [
        ChatMessage(role=MessageRole.SYSTEM, content=SYSTEM_PROMPT),
        ChatMessage(role=MessageRole.USER, content=user_prompt),
    ]

    llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}",
        request_timeout=120.0,
    )

    try:
        for chunk in llm.stream_chat(messages):
            yield chunk.delta
    except ConnectionRefusedError as e:
        logger.error("Ollama connection refused: %s", e)
        yield f"Error: Could not connect to Ollama at {OLLAMA_HOST}:{OLLAMA_PORT}. Is the Ollama container running?"
    except Exception as e:
        logger.error("Ollama request failed: %s", e)
        yield f"Error: Ollama request failed — {e}"

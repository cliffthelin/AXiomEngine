#!/usr/bin/env python3
"""
AXIOMENGINE PERSISTENT CONVERSATIONAL MEMORY (Phase 7)

Addresses "assistant amnesia": every chat turn processed by the router is
persisted to `conversation_memory` (best-effort, never blocking the reply),
and can be recalled later by semantic similarity (pgvector) with a full-text
(FTS) fallback when the embedding backend is unavailable — e.g. across a
process restart or a brand-new session asking about something discussed days
earlier.
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Optional

import asyncpg
import httpx

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


async def _get_embedding(text: str) -> Optional[List[float]]:
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(OLLAMA_URL, json={"model": EMBED_MODEL, "prompt": text})
            resp.raise_for_status()
            return resp.json()["embedding"]
    except Exception:
        return None  # semantic recall degrades to FTS-only; never fatal


async def save_turn(session_id: str, agent_name: str, role: str, content: str) -> None:
    """Persist one conversational turn. Swallows all errors: memory is
    best-effort and must never break the live chat path."""
    if not content or not content.strip():
        return
    try:
        embedding = await _get_embedding(content)
        conn = await asyncpg.connect(PG_DSN)
        try:
            await conn.execute(
                "INSERT INTO conversation_memory (session_id, agent_name, role, content, embedding) "
                "VALUES ($1, $2, $3, $4, $5)",
                session_id, agent_name, role, content,
                str(embedding) if embedding else None,
            )
        finally:
            await conn.close()
    except Exception as e:
        print(f"ConversationMemory: save_turn failed (non-fatal): {e}")


async def recall(query: str, session_id: Optional[str] = None, limit: int = 5) -> List[Dict]:
    """Recall prior turns relevant to `query`. Uses vector similarity when an
    embedding is available, otherwise falls back to Postgres full-text search."""
    conn = await asyncpg.connect(PG_DSN)
    try:
        embedding = await _get_embedding(query)
        if embedding:
            if session_id:
                rows = await conn.fetch(
                    """SELECT session_id, agent_name, role, content, created_at,
                              1 - (embedding <=> $1::vector) as similarity
                       FROM conversation_memory
                       WHERE embedding IS NOT NULL AND session_id = $2
                       ORDER BY embedding <=> $1::vector LIMIT $3""",
                    str(embedding), session_id, limit,
                )
            else:
                rows = await conn.fetch(
                    """SELECT session_id, agent_name, role, content, created_at,
                              1 - (embedding <=> $1::vector) as similarity
                       FROM conversation_memory
                       WHERE embedding IS NOT NULL
                       ORDER BY embedding <=> $1::vector LIMIT $2""",
                    str(embedding), limit,
                )
        else:
            if session_id:
                rows = await conn.fetch(
                    """SELECT session_id, agent_name, role, content, created_at,
                              ts_rank(content_tsv, plainto_tsquery('english', $1)) as similarity
                       FROM conversation_memory
                       WHERE content_tsv @@ plainto_tsquery('english', $1) AND session_id = $2
                       ORDER BY similarity DESC LIMIT $3""",
                    query, session_id, limit,
                )
            else:
                rows = await conn.fetch(
                    """SELECT session_id, agent_name, role, content, created_at,
                              ts_rank(content_tsv, plainto_tsquery('english', $1)) as similarity
                       FROM conversation_memory
                       WHERE content_tsv @@ plainto_tsquery('english', $1)
                       ORDER BY similarity DESC LIMIT $2""",
                    query, limit,
                )
        return [dict(r) for r in rows]
    finally:
        await conn.close()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 conversation_memory.py <query> [session_id]")
        return
    query = sys.argv[1]
    session_id = sys.argv[2] if len(sys.argv) > 2 else None
    results = await recall(query, session_id=session_id)
    for r in results:
        print(f"({r['similarity']:.3f}) [{r['role']}/{r['agent_name']}] {r['content'][:120]}")


if __name__ == "__main__":
    asyncio.run(main())

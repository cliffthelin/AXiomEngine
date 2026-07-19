#!/usr/bin/env python3
import asyncio
import asyncpg
import httpx
import sys
from typing import List, Dict

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
MODEL = "nomic-embed-text"

async def get_embedding(text: str) -> List[float]:
    async with httpx.AsyncClient() as client:
        resp = await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
        resp.raise_for_status()
        return resp.json()["embedding"]

async def search_context(query: str, limit: int = 5) -> Dict:
    emb = await get_embedding(query)
    conn = await asyncpg.connect(PG_DSN)

    results = {
        "projects": [],
        "pdd_rules": [],
        "memory": [],
        "user_profile": None
    }

    # Persistent Conversational Memory: recall prior turns relevant to this query
    memory_rows = await conn.fetch("""
        SELECT session_id, agent_name, role, content, created_at,
               1 - (embedding <=> $1::vector) as similarity
        FROM conversation_memory
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> $1::vector
        LIMIT 3
    """, str(emb))

    for r in memory_rows:
        results["memory"].append({
            "session_id": r['session_id'],
            "agent_name": r['agent_name'],
            "role": r['role'],
            "content": r['content'],
            "similarity": float(r['similarity'])
        })

    # User Intelligence: self-declared role/expectations/lingo, if an interview was run
    profile_row = await conn.fetchrow(
        "SELECT job_role, expectations, company_lingo FROM user_profile "
        "WHERE user_id = 'default' AND interviewed_at IS NOT NULL"
    )
    if profile_row:
        results["user_profile"] = {
            "job_role": profile_row["job_role"],
            "expectations": profile_row["expectations"],
            "company_lingo": profile_row["company_lingo"],
        }

    # Search projects
    rows = await conn.fetch("""
        SELECT path, filename, content, 
               1 - (embedding <=> $1::vector) as similarity
        FROM project_index
        ORDER BY embedding <=> $1::vector
        LIMIT $2
    """, str(emb), limit)
    
    for r in rows:
        results["projects"].append({
            "path": r['path'],
            "filename": r['filename'],
            "similarity": float(r['similarity']),
            "snippet": r['content'][:500] + "..." if len(r['content']) > 500 else r['content']
        })

    # Search PDD rules
    rules = await conn.fetch("""
        SELECT rule_id, title, content,
               1 - (embedding <=> $1::vector) as similarity
        FROM pdd_rules
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> $1::vector
        LIMIT 3
    """, str(emb))
    
    for r in rules:
        results["pdd_rules"].append({
            "rule_id": r['rule_id'],
            "title": r['title'],
            "content": r['content'],
            "similarity": float(r['similarity'])
        })

    await conn.close()
    return results

async def main():
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "gpu thermal limits"
    res = await search_context(query)
    
    print(f"\nSearch results for: '{query}'")
    print("="*60)
    
    print("\n[Project Files]")
    for p in res["projects"]:
        print(f"  ({p['similarity']:.3f}) {p['path']}")
    
    print("\n[PDD Rules]")
    for r in res["pdd_rules"]:
        print(f"  ({r['similarity']:.3f}) {r['rule_id']}: {r['title']}")

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
AXIOMENGINE PI RULE EXTENSIONS INDEXER (Phase 7)

Discovers installed PI extensions (scripts/extension_manager.py), collects
any PDD rules they contribute via `pi.registerRuleProvider(scope, handler)`,
embeds them, and upserts them into `pdd_rules`. Once indexed there, they
flow through the existing rule-injection pipeline (`router/main.py
get_pdd_rules` + `inject_pdd_context`) exactly like any core rule scoped to
the same agent — no separate injection path needed.

Run after installing/updating an extension that contributes rules, or on a
schedule (e.g. via cron/heartbeat) to keep the index current.
"""
import asyncio
import sys
from pathlib import Path

import asyncpg
import httpx

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.extension_manager import ExtensionManager

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


async def _get_embedding(text: str):
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(OLLAMA_URL, json={"model": EMBED_MODEL, "prompt": text})
        resp.raise_for_status()
        return resp.json()["embedding"]


async def index_extension_rules(project_dir: str = ".") -> int:
    manager = ExtensionManager()
    manager.discover_extensions(project_dir)
    rules = await manager.collect_rules()

    if not rules:
        print("PI Rule Extensions: no extension-contributed rules found.")
        return 0

    conn = await asyncpg.connect(PG_DSN)
    indexed = 0
    try:
        for rule in rules:
            try:
                embedding = await _get_embedding(f"{rule.get('title', '')}\n{rule['content']}")
            except Exception as e:
                print(f"PI Rule Extensions: embedding failed for {rule['rule_id']}: {e}")
                embedding = None

            await conn.execute(
                """INSERT INTO pdd_rules (rule_id, scope, title, content, embedding, active)
                   VALUES ($1, $2, $3, $4, $5, TRUE)
                   ON CONFLICT (rule_id) DO UPDATE SET
                     scope = $2, title = $3, content = $4, embedding = $5,
                     version = pdd_rules.version + 1, updated_at = NOW()""",
                rule["rule_id"], rule["scope"], rule["title"], rule["content"],
                str(embedding) if embedding else None,
            )
            indexed += 1
            print(f"PI Rule Extensions: indexed {rule['rule_id']} (scope={rule['scope']}).")
    finally:
        await conn.close()

    return indexed


if __name__ == "__main__":
    count = asyncio.run(index_extension_rules())
    print(f"PI Rule Extensions: {count} rule(s) indexed.")

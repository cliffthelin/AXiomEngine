#!/usr/bin/env python3
import asyncio
import hashlib
import os
from pathlib import Path
import httpx
import asyncpg

# Config
PROJECTS_DIR = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects")
PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"
MODEL = "nomic-embed-text"

# Extensions to index
EXTENSIONS = {'.md', '.py', '.sh', '.json', '.yml', '.yaml', '.txt', '.conf'}
IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.axiomengine_venv', 
    'cache', '.context', 'backups', 'env', 'Lib', 'site-packages', 
    '.ipynb_checkpoints', '.pytest_cache', 'dist', 'build', 'target'
}

async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60.0) as client:
        for i in range(3):
            try:
                resp = await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": text})
                if resp.status_code == 200:
                    return resp.json()["embedding"]
                print(f"  Embedding failed ({resp.status_code}) for text length {len(text)}, retry {i+1}...")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"  Embedding exception: {e}, retry {i+1}...")
                await asyncio.sleep(2)
        raise Exception("Failed to get embedding after retries")

async def index_pdd_rules(conn):
    print("Updating PDD rules with embeddings...")
    rules = await conn.fetch("SELECT rule_id, content FROM pdd_rules WHERE embedding IS NULL")
    for r in rules:
        try:
            emb = await get_embedding(r['content'])
            await conn.execute("UPDATE pdd_rules SET embedding = $1 WHERE rule_id = $2", str(emb), r['rule_id'])
            print(f"  Indexed PDD: {r['rule_id']}")
        except Exception as e:
            print(f"  Error indexing PDD {r['rule_id']}: {e}")

async def setup_project_index(conn):
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS project_index (
            id SERIAL PRIMARY KEY,
            path TEXT NOT NULL UNIQUE,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding vector(768),
            file_hash TEXT,
            last_indexed TIMESTAMPTZ DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS project_index_embedding_idx 
        ON project_index USING hnsw (embedding vector_cosine_ops);
    """)

async def index_projects(conn):
    print(f"Indexing projects in {PROJECTS_DIR}...")
    for root, dirs, files in os.walk(PROJECTS_DIR):
        # Prune ignore dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            path = Path(root) / file
            if path.suffix not in EXTENSIONS:
                continue
            
            try:
                content = path.read_text(errors='ignore')
                if not content.strip():
                    continue
                
                # Simple hashing to avoid re-indexing
                file_hash = hashlib.sha256(content.encode()).hexdigest()
                
                existing = await conn.fetchrow(
                    "SELECT id FROM project_index WHERE path = $1 AND file_hash = $2",
                    str(path), file_hash
                )
                if existing:
                    # print(f"  Skipping (unchanged): {path.name}")
                    continue
                
                print(f"  Indexing: {path.relative_to(PROJECTS_DIR)}")
                
                # For now, index the whole file. If it's too big, we should chunk it.
                # But for a start, this is fine.
                index_content = content
                if len(content) > 4000: # Lowered cap to avoid overloading embedding model
                    index_content = content[:4000]
                
                emb = await get_embedding(index_content)
                
                await conn.execute("""
                    INSERT INTO project_index (path, filename, content, embedding, file_hash)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (path) DO UPDATE 
                    SET content = EXCLUDED.content, 
                        embedding = EXCLUDED.embedding, 
                        file_hash = EXCLUDED.file_hash,
                        last_indexed = NOW()
                """, str(path), file, content, str(emb), file_hash)
                
            except Exception as e:
                print(f"  Error indexing {path}: {e}")

async def main():
    try:
        conn = await asyncpg.connect(PG_DSN)
        print("Connected to Postgres")
    except Exception as e:
        print(f"Failed to connect to Postgres: {e}")
        return

    await setup_project_index(conn)
    await index_pdd_rules(conn)
    await index_projects(conn)
    await conn.close()
    print("Indexing complete.")

if __name__ == "__main__":
    asyncio.run(main())

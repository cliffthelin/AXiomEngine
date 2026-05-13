#!/usr/bin/env python3
"""
AXiomEngine Central Router / Gateway
=================================
Single entry point for all agent traffic. Enforces PDD governance,
routes to correct backend (Mode 1-3), injects rules context, and
maintains audit trail.

Port: 9001
"""
import asyncio
import hashlib
import json
import time
import os
import subprocess
import uuid
from typing import Optional

import asyncpg
import httpx
import uvicorn
import redis
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import sys
from pathlib import Path

# Add project root to path for imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "core"))
sys.path.append(str(ROOT_DIR / "scripts"))

from stitch import Stitch
from core.cache.response_state_cache import global_response_cache

# ── Config ────────────────────────────────────────────────────────────────────
BACKENDS = {
    "split":   "http://127.0.0.1:8330",   # Nemotron snap (P40+3070 split)
    "ollama":  "http://127.0.0.1:11434",   # Ollama (Qwen 3.6 35B)
    "p40":     "http://127.0.0.1:8081",    # Mode 3: P40 direct
    "3070":    "http://127.0.0.1:8082",    # Mode 3: 3070 direct
}

MODEL_ROUTES = {
    "nemotron":  "split",
    "qwen3.6":   "ollama",
    "qwen3":     "ollama",
    "gemma":     "split",
    "kimiko":    "ollama",
    "default":   "split",
}

PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
VALKEY_HOST = "127.0.0.1"
VALKEY_PORT = 6379

app = FastAPI(title="AXiomEngine Router")
stitch = Stitch()

# ── State ─────────────────────────────────────────────────────────────────────
pg_pool: Optional[asyncpg.Pool] = None
valkey_client = stitch.client

@app.on_event("startup")
async def startup():
    global pg_pool, valkey_client
    try:
        pg_pool = await asyncpg.create_pool(os.getenv("DATABASE_URL", "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"))
        valkey_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        print("Router: Connected to Postgres and Valkey")
        
        # --- EXTENSION EVENT BUS ---
        from scripts.extension_manager import get_manager
        mgr = get_manager()
        await mgr.api.emit("session_start", {"reason": "startup"})
        print("Router: Extension Manager initialized.")
        
    except Exception as e:
        print(f"Router Startup Error: {e}")

@app.on_event("shutdown")
async def shutdown():
    if pg_pool:
        await pg_pool.close()

# ── Helpers ───────────────────────────────────────────────────────────────────
def select_backend(body: dict) -> str:
    model = (body.get("model") or "").lower()
    tags = body.get("tags") or []
    if "p40_only" in tags: return "p40"
    if "3070_only" in tags: return "3070"
    for prefix, backend in MODEL_ROUTES.items():
        if model.startswith(prefix): return backend
    return MODEL_ROUTES["default"]

def prompt_hash(body: dict) -> str:
    msgs = json.dumps(body.get("messages", []), sort_keys=True)
    return hashlib.sha256(msgs.encode()).hexdigest()[:16]

async def get_pdd_rules(scope: str = "core") -> list[dict]:
    if not pg_pool: return []
    async with pg_pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT rule_id, title, content FROM pdd_rules WHERE active = TRUE AND (scope = $1 OR scope = 'core') ORDER BY rule_id LIMIT 10",
            scope
        )
    return [dict(r) for r in rows]

def inject_pdd_context(body: dict, rules: list[dict]) -> dict:
    if not rules: return body
    rule_text = "\n".join(f"[{r['rule_id']}] {r.get('title', '')}: {r['content'][:200]}" for r in rules)
    system_msg = {"role": "system", "content": f"You are operating under PDD governance. Rules:\n{rule_text}"}
    msgs = body.get("messages", [])
    if msgs and msgs[0].get("role") == "system":
        msgs[0]["content"] = system_msg["content"] + "\n\n" + msgs[0]["content"]
    else:
        msgs = [system_msg] + msgs
    return {**body, "messages": msgs}

async def audit_log(session_id: str, agent: str, model: str, backend: str, rules: list, in_hash: str, out_hash: str, t_in: int, t_out: int, lat: int):
    if not pg_pool: return
    async with pg_pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO agent_audit (session_id, agent_name, model, rules_cited, prompt_hash, output_hash, backend, tokens_in, tokens_out, latency_ms) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)",
            session_id, agent, model, [r["rule_id"] for r in rules], in_hash, out_hash, backend, t_in, t_out, lat
        )

# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "postgres": pg_pool is not None, "valkey": valkey_client is not None}

@app.get("/admin/audit")
async def get_audit(limit: int = 50):
    if not pg_pool: return []
    async with pg_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM agent_audit ORDER BY created_at DESC LIMIT $1", limit)
    return [dict(r) for r in rows]

@app.get("/admin/test-results")
async def get_test_results():
    results = stitch.client.get("axiomengine:test_harness:last_results")
    last_run = stitch.client.get("axiomengine:test_harness:last_run")
    return {"results": json.loads(results) if results else [], "last_run": last_run.decode() if last_run else None}

@app.post("/admin/run-tests")
async def run_tests():
    venv_python = os.path.expanduser("~/.axiomengine_venv/bin/python")
    script_path = "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/scripts/archon_tester.py"
    subprocess.Popen([venv_python, script_path])
    return {"status": "started"}

@app.get("/admin/kg-stats")
async def get_kg_stats():
    kg_path = "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/knowledge_graph.json"
    if os.path.exists(kg_path):
        with open(kg_path, "r") as f:
            data = json.load(f)
            return {"nodes": len(data.get("nodes", [])), "edges": len(data.get("edges", []))}
    return {"nodes": 0, "edges": 0}
    
@app.post("/admin/extensions/plannotator/review")
async def trigger_plannotator_review():
    from scripts.extension_manager import get_manager
    mgr = get_manager()
    # In a real setup, we'd identify the active session
    # For now, we trigger a global review command
    result = await mgr.api.emit("command:plannotator-review", {"input": ""})
    return {"status": "ok", "url": result.get("output", ""), "message": result.get("message", "")}

@app.get("/admin/dashboard")
async def dashboard(request: Request):
    template_path = os.path.join(os.path.dirname(__file__), "templates/dashboard.html")
    with open(template_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/admin/settings")
async def settings(request: Request):
    template_path = os.path.join(os.path.dirname(__file__), "templates/settings.html")
    with open(template_path, "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/admin/proposals")
async def get_proposals(status: str = "pending"):
    if not pg_pool: return []
    async with pg_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM pdd_proposals WHERE status = $1 ORDER BY created_at DESC", status)
    return [dict(r) for r in rows]

@app.post("/admin/proposals/{pid}/{action}")
async def resolve_proposal(pid: int, action: str):
    if not pg_pool: return {"error": "DB down"}
    if action not in ["approve", "reject"]:
        raise HTTPException(400, "Invalid action")
    
    status = "approved" if action == "approve" else "rejected"
    async with pg_pool.acquire() as conn:
        # Update proposal status
        await conn.execute("UPDATE pdd_proposals SET status = $1, updated_at = NOW() WHERE proposal_id = $2", status, pid)
        
        if action == "approve":
            # If approved, promote to pdd_rules
            prop = await conn.fetchrow("SELECT * FROM pdd_proposals WHERE proposal_id = $1", pid)
            if prop['change_type'] == 'new':
                await conn.execute(
                    "INSERT INTO pdd_rules (rule_id, title, content, scope) VALUES ($1, $2, $3, 'swarm') ON CONFLICT (rule_id) DO UPDATE SET content=$3, title=$2",
                    prop['rule_id'], prop['title'], prop['content']
                )
            elif prop['change_type'] == 'update':
                await conn.execute(
                    "UPDATE pdd_rules SET content = $1, title = $2, updated_at = NOW() WHERE rule_id = $3",
                    prop['content'], prop['title'], prop['rule_id']
                )
            elif prop['change_type'] == 'delete':
                await conn.execute("UPDATE pdd_rules SET active = FALSE WHERE rule_id = $1", prop['rule_id'])
                
    return {"status": status}

@app.websocket("/v1/realtime")
async def realtime_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = websocket.headers.get("X-Session-Id", str(uuid.uuid4()))
    session = global_response_cache.get_session(session_id) or global_response_cache.create_session(session_id)
    session.connection_id = str(uuid.uuid4())
    
    print(f"Realtime: Session {session_id} connected (CID: {session.connection_id})")
    
    try:
        while True:
            data = await websocket.receive_json()
            # Process realtime turn
            t_start = time.monotonic()
            
            # Use session cache to rehydrate context
            if "messages" in data:
                # Append new messages to session cache
                session.conversation_state_cache.extend(data["messages"])
            
            # Reconstruct full body for backend
            full_body = {**data, "messages": session.conversation_state_cache}
            
            backend_key = select_backend(full_body)
            backend_url = BACKENDS.get(backend_key)
            
            # Governance
            agent_name = websocket.headers.get("X-Agent-Name", "unknown").lower()
            rules = await get_pdd_rules(scope=agent_name)
            governed_body = inject_pdd_context(full_body, rules)
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(f"{backend_url}/v1/chat/completions", json=governed_body)
            
            result = resp.json()
            
            # Update session with new response id
            session.previous_response_id = result.get("id")
            session.update_activity()
            
            # Send back to agent
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        print(f"Realtime: Session {session_id} disconnected")
    except Exception as e:
        print(f"Realtime Error: {e}")
        await websocket.close()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request, bg: BackgroundTasks):
    body = await request.json()
    t_start = time.monotonic()
    backend_key = select_backend(body)
    backend_url = BACKENDS.get(backend_key)
    model = body.get("model", "nemotron")
    session_id = request.headers.get("X-Session-Id", "anon")
    agent_name = request.headers.get("X-Agent-Name", "unknown").lower()
    
    # Check session cache
    session = global_response_cache.get_session(session_id)
    if session and "messages" in body:
        # Incremental continuation: Merge session cache if body only has new messages
        # For simplicity, we just use session cache if it exists
        session.conversation_state_cache.extend(body["messages"])
        body["messages"] = session.conversation_state_cache
    elif session_id != "anon":
        # Create session for future turns
        session = global_response_cache.create_session(session_id)
        if "messages" in body:
            session.conversation_state_cache = body["messages"]

    rules = await get_pdd_rules(scope=agent_name)
    governed_body = inject_pdd_context(body, rules)

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(f"{backend_url}/v1/chat/completions", json=governed_body)
    
    result = resp.json()
    latency_ms = int((time.monotonic() - t_start) * 1000)
    
    if session:
        session.previous_response_id = result.get("id")
        session.update_activity()
    
    bg.add_task(audit_log, session_id, "router", model, backend_key, rules, "hash", "hash", 0, 0, latency_ms)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)

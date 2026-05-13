#!/usr/bin/env python3
from fastapi import FastAPI, Request, BackgroundTasks, WebSocket, WebSocketDisconnect
import uvicorn
import httpx
import sys
import json
import asyncio
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from agent_lib import AsyncAXiomEngineClient

app = FastAPI(title="AXiomEngine Remote Gateway")
stitch = Stitch()

@app.websocket("/ws/agent")
async def agent_stream(websocket: WebSocket):
    await websocket.accept()
    
    from scripts.extension_manager import get_manager
    mgr = get_manager()
    
    # Bridge UI confirm/notify to WebSocket
    async def gui_confirm(title, msg):
        await websocket.send_json({"type": "ui_confirm", "title": title, "message": msg})
        # Wait for response from GUI
        res = await websocket.receive_json()
        return res.get("value", False)
        
    client = AsyncAXiomEngineClient(name="GUI-Agent")
    # Custom UI for this session
    from scripts.extension_manager import ExtensionUI
    client.agent.ui = ExtensionUI(tui=None) # We'll bridge manually
    
    try:
        while True:
            # Expecting a JSON with "prompt"
            data = await websocket.receive_text()
            req = json.loads(data)
            prompt = req.get("prompt", "")
            
            async for event in client.agent.prompt(prompt):
                # Standard AgentLoopEvent.dict()
                await websocket.send_json(event.dict())
                
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Agent WS Error: {e}")

@app.post("/webhook/{agent_name}")
async def handle_webhook(agent_name: str, request: Request, background_tasks: BackgroundTasks):
    """
    Real Webhook Gateway.
    Receives external triggers and injects them into the Stitch bus.
    """
    data = await request.json()
    print(f"Gateway: Received remote command for {agent_name}")
    
    # Inject into Stitch
    stitch.send_task(agent_name, "REMOTE_COMMAND", data, sender="remote_gateway")
    
    return {"status": "queued", "agent": agent_name}

@app.post("/mcp/v1/tools/list")
async def mcp_list_tools():
    """MCP Standard: List available tools."""
    from extension_manager import get_manager
    mgr = get_manager()
    # Combine internal tools and extension tools
    tools = mgr.api.registered_tools
    return {"tools": tools}

@app.post("/mcp/v1/tools/call")
async def mcp_call_tool(request: Request):
    """MCP Standard: Call a specific tool."""
    data = await request.json()
    tool_name = data.get("name")
    tool_args = data.get("arguments", {})
    
    from extension_manager import get_manager
    mgr = get_manager()
    
    # Emit as a command event
    result = await mgr.emit(f"command:{tool_name}", {"input": str(tool_args)})
    return {"content": [{"type": "text", "text": result.get("message", "Success")}]}

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time system log streaming."""
    await websocket.accept()
    try:
        # Subscribe to Stitch bus events
        async for msg in stitch.subscribe("axiomengine:logs:*"):
            await websocket.send_text(msg)
    except Exception as e:
        print(f"WS Error: {e}")
    finally:
        await websocket.close()

@app.post("/agent/compact")
async def compact_session():
    """Manual compaction trigger for the GUI."""
    client = AsyncAXiomEngineClient(name="GUI-Agent")
    from scripts.compaction_manager import CompactionManager
    from scripts.pi_ai import stream as ai_stream
    cm = CompactionManager(ai_stream)
    await cm.compact_session(client.agent.state, client.agent.state.model)
    return {"status": "success", "message": "Session compacted"}

@app.get("/agent/models/list")
async def get_agent_models():
    from scripts.pi_ai import registry
    return [m.dict() for m in registry.models.values()]

@app.get("/agent/settings/keybindings")
async def get_agent_keybindings():
    from scripts.pi_config import get_keybindings
    return get_keybindings()

@app.get("/agent/settings/shell")
async def get_agent_shell():
    from scripts.shell_utils import get_bash_path
    return {"path": get_bash_path()}

@app.get("/agent/packages/list")
async def get_agent_packages():
    from scripts.package_manager import PackageManager
    pm = PackageManager()
    # Simplified list from git directory for now
    packages = []
    if pm.git_dir.exists():
        for d in pm.git_dir.iterdir():
            if d.is_dir():
                packages.append({"name": d.name, "source": f"git:{d.name}", "type": "git"})
    return packages

@app.get("/agent/sessions/list")
async def get_agent_sessions():
    from scripts.session_manager import SessionManager
    sm = SessionManager()
    return sm.list_project_sessions()

@app.post("/agent/sessions/export")
async def export_agent_session():
    from scripts.session_manager import SessionManager
    sm = SessionManager()
    path = sm.export_html()
    return {"status": "success", "path": path}

@app.get("/agent/settings")
async def get_agent_settings():
    from scripts.settings_manager import get_settings_manager
    return get_settings_manager().settings

@app.post("/agent/settings")
async def update_agent_settings(data: Dict[str, Any]):
    from scripts.settings_manager import get_settings_manager
    sm = get_settings_manager()
    for k, v in data.items():
        sm.set(k, v)
    return {"status": "success"}

@app.get("/agent/artifacts/{artifact_id}")
async def get_artifact(artifact_id: str):
    """Retrieve and serve sandboxed artifacts (HTML/SVG/MD)."""
    from scripts.pi_config import get_agent_dir
    art_path = get_agent_dir() / "artifacts" / f"{artifact_id}.html"
    if art_path.exists():
        with open(art_path, "r") as f:
            return {"id": artifact_id, "type": "html", "content": f.read()}
    return {"error": "Not found"}, 404

@app.get("/agent/proxy")
async def cors_proxy(url: str):
    """Browser CORS proxy for PI Web UI parity."""
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.content

@app.get("/agent/storage/{store_name}")
async def get_storage(store_name: str):
    """Server-side bridge for IndexedDB-backed Web UI stores."""
    from scripts.pi_config import get_agent_dir
    store_path = get_agent_dir() / "storage" / f"{store_name}.json"
    if store_path.exists():
        with open(store_path, "r") as f:
            return json.load(f)
    return {}

@app.get("/health")
async def health():
    return {"status": "online"}

if __name__ == "__main__":
    print("AXiomEngine Remote Gateway starting on port 9002...")
    print("MCP Endpoints active at /mcp/v1/tools/list and /mcp/v1/tools/call")
    uvicorn.run(app, host="0.0.0.0", port=9002)

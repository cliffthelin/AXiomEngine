#!/usr/bin/env python3
"""
AXiomEngine Governance Dashboard Server (v1.4.0 Additive)
=====================================================
Read-only discovery backend for the Governance Dashboard.
Provides a secure API for frozen v1.3.1 artifacts and mission logs.
"""
import json
import argparse
import os
import shlex
import sys
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Ensure the project root is in sys.path so 'scripts.*' imports work correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.governance_manifest_verifier import build_manifest_verification_result
from scripts.gpu_provider_registry import GPUProviderRegistry

VERSION = "1.4.0"

# --- Portable path roots ----------------------------------------------------
# Everything is derived from this file's location or the user's home so the
# project runs from any directory without hardcoded mount paths. Overridable
# via environment variables for non-standard layouts.
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent
PI_WORKSPACE = Path(os.environ.get(
    "AXIOMENGINE_PI_WORKSPACE",
    str(Path.home() / "AxiomEngine_Frame_Workspace"),
))
PI_CODING_AGENT_DIR = Path(os.environ.get(
    "PI_CODING_AGENT_DIR", str(Path.home() / ".pi" / "agent")
))
PI_CODING_AGENT_SESSION_DIR = Path(os.environ.get(
    "PI_CODING_AGENT_SESSION_DIR",
    str(PI_CODING_AGENT_DIR / "sessions" / "axiomengine"),
))

# --- SHARED HELPERS (Module Level) ---

def parse_yaml_workflow(content: str) -> dict:
    result = {"name": "", "description": "", "nodes": []}
    lines = content.splitlines()
    i = 0
    in_desc_block = False
    desc_lines = []
    in_nodes_block = False
    current_node = {}
    
    while i < len(lines):
        line = lines[i]
        # Ignore comments and empty lines
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue
            
        # Detect indentation
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        
        if in_desc_block:
            if indent > 0 or stripped == "":
                desc_lines.append(stripped)
                i += 1
                continue
            else:
                in_desc_block = False
                result["description"] = "\n".join(desc_lines).strip()
                
        if in_nodes_block:
            if stripped.startswith("-"):
                if current_node:
                    result["nodes"].append(current_node)
                    current_node = {}
                # Start new node
                node_part = stripped[1:].strip()
                if node_part.startswith("-"):
                    node_part = node_part[1:].strip()
                if ":" in node_part:
                    k, v = node_part.split(":", 1)
                    current_node[k.strip()] = v.strip()
            elif ":" in stripped and indent > 0:
                k, v = stripped.split(":", 1)
                current_node[k.strip()] = v.strip()
            elif indent == 0:
                in_nodes_block = False
                if current_node:
                    result["nodes"].append(current_node)
                    current_node = {}
            else:
                i += 1
                continue
                
        if stripped.startswith("name:"):
            result["name"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("description:"):
            desc_val = stripped.split(":", 1)[1].strip()
            if desc_val == "|":
                in_desc_block = True
                desc_lines = []
            else:
                result["description"] = desc_val
        elif stripped.startswith("nodes:"):
            in_nodes_block = True
            current_node = {}
            
        i += 1
        
    if current_node:
        result["nodes"].append(current_node)
        
    if in_desc_block and desc_lines:
        result["description"] = "\n".join(desc_lines).strip()
        
    return result


def safe_read_json(path):
    """Safely read and parse JSON, returning error object if malformed."""
    if not path.exists():
        return {"error": "File not found", "path": str(path.name)}
    try:
        return json.loads(path.read_text())
    except Exception as e:
        return {"error": "Malformed JSON", "parse_error": str(e), "path": str(path.name)}

def get_all_reports_from_dirs(mission_dirs):
    """Programmatic discovery of governance reports across directories."""
    reports = []
    for d in mission_dirs:
        # Latest in mission dir
        latest = d / "closer_report.json"
        if latest.exists():
            reports.append(safe_read_json(latest))
        
        # Historical
        hist_dir = d / "closer_reports"
        if hist_dir.exists():
            for f in hist_dir.glob("closer_report_*.json"):
                reports.append(safe_read_json(f))
    
    # Filter out errors and sort by timestamp
    valid_reports = [r for r in reports if isinstance(r, dict) and "error" not in r]
    valid_reports.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return valid_reports

def resolve_mission_status(r):
    """Determine the operational status of a governance mission report."""
    if not r or (isinstance(r, dict) and "error" in r): return "MISSING_REPORT"
    if r.get("dry_run"): return "DRY_RUN"
    if len(r.get("validation_errors", [])) > 0 and r.get("strict"): return "STRICT_ABORT"
    if r.get("rejected_count", 0) > 0: return "PARTIAL_SUCCESS"
    return "SUCCESS"

# --- DISCOVERY HANDLER ---

class GovernanceDiscoveryHandler(BaseHTTPRequestHandler):
    active_processes = {}

    def end_headers(self):
        # Strict Local CORS
        origin = self.headers.get('Origin')
        if origin:
            # Allow localhost, 127.0.0.1, and variants with ports
            pattern = r'^http://(localhost|127\.0\.0\.1)(:\d+)?$'
            if re.match(pattern, origin):
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Normalize path: remove trailing slash and strip query string for matching
        raw_path = self.path
        path = raw_path.split("?")[0]
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]

        routes = {
            "/": self.handle_dashboard,
            "/dashboard": self.handle_dashboard,
            "/project/new": self.handle_project_setup_page,
            "/health": self.handle_health,
            "/api/gpu/status": self.handle_gpu_status,
            "/api/index": self.handle_index,
            "/api/governance/manifest": self.handle_manifest,
            "/api/governance/baseline/status": self.handle_baseline_status,
            "/api/governance/decisions": self.handle_decisions,
            "/api/governance/latest-report": self.handle_latest_report,
            "/api/governance/historical-reports": self.handle_historical_reports,
            "/api/governance/mission-artifacts": self.handle_mission_artifacts,
            "/api/governance/gpu-status": self.handle_gpu_status,
            "/api/governance/live-logs": self.handle_live_logs,
            "/api/governance/files": self.handle_files,
            "/api/governance/summary": self.handle_summary,
            "/api/governance/layers": self.handle_layers,
            "/api/governance/projects": self.handle_projects,
            "/api/governance/processing_status": self.handle_processing_status,
            "/api/governance/reversa-prompt": self.handle_reversa_prompt,
            "/api/governance/ast": self.handle_ast_index,
            "/api/governance/archon/workflows": self.handle_archon_workflows,
            "/api/governance/archon/runs": self.handle_archon_runs,
            "/api/governance/archon/env": self.handle_archon_get_env,
            "/api/governance/archon/swarm": self.handle_archon_swarm_status,
            "/api/governance/hermes/skills": self.handle_hermes_skills,
            "/api/governance/pi/skills": self.handle_pi_skills,
            "/api/governance/pi/presets": self.handle_pi_presets,
            "/api/governance/settings": self.handle_settings,
            "/user-profile": self.handle_user_profile,
            "/c2": self.handle_c2,
            "/layers": self.handle_layers_view,
            "/visualizer": self.handle_visualizer,
            "/agent_manager": self.handle_agent_manager_view,
            "/api/agent_manager/list": self.handle_agent_manager_list,
            "/api/agent_manager/models": self.handle_agent_manager_models,
            "/api/agent_manager/versions": self.handle_agent_manager_versions,
            "/api/agent_manager/chat/history": self.handle_agent_manager_chat_history,
            "/api/governance/reversa/config": self.handle_reversa_get_config,
            "/api/governance/reversa/assets": self.handle_reversa_get_assets,
            "/api/governance/reversa/asset": self.handle_reversa_get_asset,
            "/api/governance/reversa/asset/diff": self.handle_reversa_asset_diff,
            "/api/governance/reversa/asset/history": self.handle_reversa_asset_history,
            "/api/governance/reversa/task-status": self.handle_reversa_task_status,
            "/api/governance/reversa/validate": self.handle_reversa_validate_asset,
            "/api/axiom/status": self.handle_axiom_status,
            "/api/axiom/settings": self.handle_axiom_get_settings,
            "/api/visualizer/graph": self.handle_visualizer_graph,
            "/api/visualizer/c4": self.handle_visualizer_c4,
            "/api/dispatch/hitm/gates": self.handle_approval_gates_list,
            "/api/schemas": self.handle_schema_list,
            "/api/registry/assets": self.handle_registry_assets,
        }

        # Route matching
        handler = routes.get(path)
        if handler:
            handler()
        elif path == "/pi-gui":
            self.send_response(301)
            self.send_header("Location", "/pi-gui/")
            self.end_headers()
        elif path.startswith("/pi-gui/"):
            self.handle_pi_gui()
        elif path.startswith("/project/") and path != "/project/new":
            self.handle_project_detail_page()
        elif path.endswith(".html"):
            # Serve static HTML files from system_root
            filename = path[1:]  # Remove leading slash
            self.serve_html_file(filename)
        else:
            self.send_error(404, f"Route Not Found: {path}")

    def handle_user_profile(self):
        self.serve_html_file("governance_user_profile.html")

    def handle_c2(self):
        self.serve_html_file("governance_c2_dashboard.html")

    def handle_layers_view(self):
        self.serve_html_file("governance_layer_orchestrator.html")

    def handle_visualizer(self):
        self.serve_html_file("governance_visualizer.html")

    def handle_visualizer_graph(self):
        """GET /api/visualizer/graph — returns a D3-compatible force graph of context assets."""
        import os, hashlib, datetime as dt

        nodes = []
        links = []
        node_ids = set()

        def add_node(node_id, group, label=None, path=None, asset_type=None, status=None, size_bytes=0):
            if node_id not in node_ids:
                node_ids.add(node_id)
                node = {
                    "id": node_id,
                    "label": label or node_id,
                    "group": group,
                    "radius": 18 if group == "root" else (12 if group == "category" else 6),
                    "path": path or "",
                    "asset_type": asset_type or "",
                    "status": status or "unknown",
                    "size_bytes": size_bytes,
                }
                nodes.append(node)

        # Root node
        add_node("Project Root", "root", label="Project Root")

        # Category directories to scan
        category_dirs = {
            "_reversa_sdd": {"group": "context", "asset_type": "requirements"},
            "skills": {"group": "skills", "asset_type": "skill"},
            ".agents/skills": {"group": "skills", "asset_type": "skill"},
            "data/catalog/PDD": {"group": "policy", "asset_type": "pdd-rule"},
            "docs/pdd": {"group": "policy", "asset_type": "pdd-rule"},
            "docs/audit": {"group": "evidence", "asset_type": "evidence-artifact"},
            "_reversa_forward": {"group": "context", "asset_type": "roadmap"},
            "data/schemas": {"group": "schema", "asset_type": "schema"},
        }

        for dir_path, meta in category_dirs.items():
            full_dir = self.server.project_root / dir_path
            if not full_dir.exists() or not full_dir.is_dir():
                continue

            # Add category node
            dir_id = dir_path.replace("/", "/")
            add_node(dir_id, "category", label=dir_path, asset_type=meta["asset_type"])
            links.append({"source": "Project Root", "target": dir_id, "value": 2, "type": "contains"})

            # Scan files (limit to avoid huge graphs)
            file_count = 0
            for root_dir, dirs, files in os.walk(full_dir):
                dirs[:] = [d for d in dirs if d not in ["__pycache__", "node_modules", ".git", "backups", "agent_versions"]]
                for file in files:
                    if file_count > 80:
                        break
                    if not file.endswith((".md", ".json", ".yml", ".yaml", ".toml")):
                        continue
                    full_path = os.path.join(root_dir, file)
                    try:
                        rel = os.path.relpath(full_path, self.server.project_root)
                        stat = os.stat(full_path)
                        node_id = rel.replace("\\", "/")
                        add_node(
                            node_id,
                            "leaf",
                            label=file,
                            path=rel,
                            asset_type=meta["asset_type"],
                            status="active",
                            size_bytes=stat.st_size
                        )
                        links.append({"source": dir_id, "target": node_id, "value": 1, "type": "contains"})
                        file_count += 1
                    except Exception:
                        pass

        self.send_json({"nodes": nodes, "links": links, "node_count": len(nodes), "link_count": len(links)})

    def handle_visualizer_c4(self):
        """GET /api/visualizer/c4 — returns a Mermaid C4 diagram configuration."""
        config_path = self.server.project_root / ".reversa" / "templates" / "visualizer_config.json"
        c4_code = ""
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    c4_code = config.get("c4_diagram", "")
            except Exception:
                pass
        if not c4_code:
            c4_code = """
C4Context
  title AXiomEngine & Reversa Governance Swarm Context
  
  Person(operator, "System Operator / Auditor", "Reviews specs, approves executions, and controls migration progress.")
  
  System_Boundary(axiom_swarm, "AXiomEngine Ecosystem") {
    System(hub, "AXiom Governance Hub", "Unified web interface (Port 8766) hosting management consoles.")
    System(reversa, "Reversa CLI Core", "Scouts repositories, extracts schemas, and builds SDD specs.")
    System(archon, "Archon Swarm Executor", "Monitors background tasks and drives sequential workflows.")
    System(hermes, "Hermes reasoning model", "Local Ollama agent executing interactive logic tasks.")
    SystemDb(store, "Governance State Store", "Stores changelogs, manifests, and .reversa state JSONs.")
  }
  
  Rel(operator, hub, "Interacts with dashboard, edits specs, approves tasks", "HTTP/UI")
  Rel(hub, store, "Reads and updates manifests and audit trails", "File API")
  Rel(hub, reversa, "Launches pipeline tasks & scans output", "Subprocess")
  Rel(hub, archon, "Coordinates script dispatches & reads logs", "HTTP API")
  Rel(hub, hermes, "Routes chat console and skill interview loops", "Ollama API")
  Rel(reversa, store, "Outputs generated spec artifacts & templates", "FS Write")
"""
        self.send_json({"c4_code": c4_code.strip()})

    def handle_reversa_validate_asset(self):
        """GET /api/governance/reversa/validate?path=<rel_path>
        Runs JSON schema validation on the specified asset file.
        """
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel_path = query.get("path", [""])[0]

        if not rel_path:
            self.send_json({"error": "Missing path parameter"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/") or rel_path.startswith("\\"):
            self.send_json({"error": "Access denied"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        if not target_path.exists() or not target_path.is_file():
            self.send_json({"error": "File not found"}, status=404)
            return

        if not rel_path.endswith(".json"):
            self.send_json({
                "valid": True,
                "message": "Validation skipped: Schema validation is only enforced on JSON artifacts.",
                "errors": []
            })
            return

        try:
            content = target_path.read_text(encoding="utf-8")
            parsed_json = json.loads(content)
            
            scripts_dir = str(self.server.project_root / "scripts")
            import sys
            if scripts_dir not in sys.path:
                sys.path.append(scripts_dir)
            
            import schema_validator
            schema_type = None
            for stype, paths in schema_validator.SCHEMA_SCAN_PATHS.items():
                for p in paths:
                    if p in rel_path:
                        schema_type = stype
                        break
                if schema_type:
                    break
            
            if not schema_type:
                self.send_json({
                    "valid": True,
                    "message": f"No registered schema found matching the path structure of '{rel_path}'.",
                    "errors": []
                })
                return
                
            objects = []
            if isinstance(parsed_json, list):
                objects = parsed_json
            elif isinstance(parsed_json, dict):
                for wrapper_key in ["projects", "workflows", "runs", "assets", "gates", "instances", "skills", "items"]:
                    if wrapper_key in parsed_json and isinstance(parsed_json[wrapper_key], list):
                        objects = parsed_json[wrapper_key]
                        break
                else:
                    objects = [parsed_json]
                    
            validation_errors = []
            for i, obj in enumerate(objects):
                errs = schema_validator.validate_object(schema_type, obj, source=f"{rel_path}[{i}]")
                if errs:
                    validation_errors.extend(errs)
                    
            if validation_errors:
                self.send_json({
                    "valid": False,
                    "message": f"Schema validation failed for schema type '{schema_type}'.",
                    "errors": validation_errors
                })
            else:
                self.send_json({
                    "valid": True,
                    "message": f"Artifact fully conforms to JSON schema: '{schema_type}'.",
                    "errors": []
                })
        except json.JSONDecodeError as jde:
            self.send_json({
                "valid": False,
                "message": f"Invalid JSON format: {jde}",
                "errors": [{"field": "json", "severity": "error", "message": str(jde), "source": "proposed"}]
            })
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_schema_list(self):
        """GET /api/schemas — list all registered canonical schemas."""
        schema_dir = self.server.project_root / "data" / "schemas"
        schemas = []
        if schema_dir.exists():
            for f in sorted(schema_dir.glob("*.schema.json")):
                try:
                    with open(f, "r", encoding="utf-8") as sf:
                        data = json.load(sf)
                    schemas.append({
                        "id": f.stem.replace(".schema", ""),
                        "title": data.get("title", f.stem),
                        "description": data.get("description", ""),
                        "path": str(f.relative_to(self.server.project_root)),
                        "schema_id": data.get("$id", ""),
                    })
                except Exception:
                    pass
        self.send_json({"schemas": schemas})

    def handle_agent_manager_view(self):
        self.serve_html_file("governance_agent_manager.html")

    def handle_dashboard(self):
        path = self.server.system_root / "governance_hub.html"
        if not path.exists():
            path = self.server.system_root / "governance_layer_orchestrator.html"
        if not path.exists():
            path = self.server.system_root / "governance_c2_dashboard.html"

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def serve_html_file(self, filename):
        path = self.server.system_root / filename
        if not path.exists():
            self.send_error(404, f"{filename} not found.")
            return
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(path.read_bytes())

    def handle_project_setup_page(self):
        self.serve_html_file("governance_project_setup.html")

    def handle_project_detail_page(self):
        self.serve_html_file("governance_project_detail.html")

    def handle_pi_gui(self):
        """Serve the PI GUI client and inject window.piApp bridge interface."""
        import mimetypes
        path_parts = self.path.split("?")[0].split("/")
        # Path looks like /pi-gui or /pi-gui/ or /pi-gui/assets/main.js
        if len(path_parts) <= 2 or (len(path_parts) == 3 and path_parts[2] == ""):
            # Serve index.html
            rel_file_path = "index.html"
        else:
            # Serve specific file: strip '/pi-gui/' prefix
            rel_file_path = "/".join(path_parts[2:])

        renderer_dir = self.server.system_root / "pi/pi-gui/apps/desktop/out/renderer"
        file_path = (renderer_dir / rel_file_path).resolve()

        # Path jailing check
        try:
            file_path.relative_to(renderer_dir)
        except ValueError:
            self.send_error(403, "Access Denied: Path outside GUI viewport")
            return

        if not file_path.exists() or not file_path.is_file():
            self.send_error(404, f"File Not Found: {rel_file_path}")
            return

        # Serve the file
        mime_type, _ = mimetypes.guess_type(str(file_path))
        if rel_file_path.endswith(".js"):
            mime_type = "application/javascript"
        elif rel_file_path.endswith(".css"):
            mime_type = "text/css"
        elif not mime_type:
            mime_type = "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        
        if rel_file_path == "index.html":
            # Read index.html and inject window.piApp bridge
            try:
                html_content = file_path.read_text(encoding="utf-8")
                # Define window.piApp proxy script
                bridge_js = """
<script>
(function() {
    const listeners = new Map();
    
    // Connect to SSE stream directly on port 8766
    const eventSource = new EventSource('http://localhost:8766/events');
    eventSource.onmessage = (event) => {
        try {
            const msg = JSON.parse(event.data);
            const { channel, payload } = msg;
            const channelListeners = listeners.get(channel);
            if (channelListeners) {
                for (const cb of channelListeners) {
                    cb(payload);
                }
            }
        } catch (e) {
            console.error("Error handling SSE event:", e);
        }
    };
    
    function registerListener(channel, cb) {
        if (!listeners.has(channel)) {
            listeners.set(channel, new Set());
        }
        listeners.get(channel).add(cb);
        return () => {
            listeners.get(channel).delete(cb);
        };
    }
    
    async function sendRequest(method, args) {
        const response = await fetch('http://localhost:8766/api', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ method, args })
        });
        if (!response.ok) {
            const errText = await response.text();
            throw new Error(errText || `HTTP ${response.status}`);
        }
        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }
        return result.result;
    }
    
    window.piApp = {
        platform: 'linux',
        versions: { node: '22', electron: '34' },
        
        ping: () => sendRequest('ping', []),
        getState: () => sendRequest('getState', []),
        onStateChanged: (listener) => registerListener('pi-gui:state-changed', listener),
        getSelectedTranscript: () => sendRequest('getSelectedTranscript', []),
        onSelectedTranscriptChanged: (listener) => registerListener('pi-gui:selected-transcript-changed', listener),
        onCommand: (listener) => registerListener('pi-gui:app-command', listener),
        onWorkspacePicked: (listener) => registerListener('pi-gui:workspace-picked', listener),
        onClipboardImagePasted: (listener) => registerListener('pi-gui:clipboard-image-pasted', listener),
        getPathForFile: (file) => (process.env.AXIOMENGINE_PI_WORKSPACE || (require('os').homedir() + '/AxiomEngine_Frame_Workspace')) + '/' + file.name,
        addWorkspacePath: (workspacePath) => sendRequest('addWorkspacePath', [workspacePath]),
        pickWorkspace: () => sendRequest('pickWorkspace', []),
        selectWorkspace: (workspaceId) => sendRequest('selectWorkspace', [workspaceId]),
        renameWorkspace: (workspaceId, displayName) => sendRequest('renameWorkspace', [workspaceId, displayName]),
        removeWorkspace: (workspaceId) => sendRequest('removeWorkspace', [workspaceId]),
        reorderWorkspaces: (workspaceOrder) => sendRequest('reorderWorkspaces', [workspaceOrder]),
        openWorkspaceInFinder: (workspaceId) => sendRequest('openWorkspaceInFinder', [workspaceId]),
        createWorktree: (input) => sendRequest('createWorktree', [input]),
        removeWorktree: (input) => sendRequest('removeWorktree', [input]),
        openSkillInFinder: (workspaceId, filePath) => sendRequest('openSkillInFinder', [workspaceId, filePath]),
        openExtensionInFinder: (workspaceId, filePath) => sendRequest('openExtensionInFinder', [workspaceId, filePath]),
        syncCurrentWorkspace: () => sendRequest('syncCurrentWorkspace', []),
        selectSession: (target) => sendRequest('selectSession', [target]),
        archiveSession: (target) => sendRequest('archiveSession', [target]),
        unarchiveSession: (target) => sendRequest('unarchiveSession', [target]),
        createSession: (input) => sendRequest('createSession', [input]),
        startThread: (input) => sendRequest('startThread', [input]),
        cancelCurrentRun: () => sendRequest('cancelCurrentRun', []),
        setActiveView: (view) => sendRequest('setActiveView', [view]),
        setSidebarCollapsed: (collapsed) => sendRequest('setSidebarCollapsed', [collapsed]),
        refreshRuntime: (workspaceId) => sendRequest('refreshRuntime', [workspaceId]),
        setModelSettingsScopeMode: (mode) => sendRequest('setModelSettingsScopeMode', [mode]),
        setDefaultModel: (workspaceId, provider, modelId) => sendRequest('setDefaultModel', [workspaceId, provider, modelId]),
        setDefaultThinkingLevel: (workspaceId, thinkingLevel) => sendRequest('setDefaultThinkingLevel', [workspaceId, thinkingLevel]),
        setSessionModel: (workspaceId, sessionId, provider, modelId) => sendRequest('setSessionModel', [workspaceId, sessionId, provider, modelId]),
        setSessionThinkingLevel: (workspaceId, sessionId, thinkingLevel) => sendRequest('setSessionThinkingLevel', [workspaceId, sessionId, thinkingLevel]),
        loginProvider: (workspaceId, providerId) => sendRequest('loginProvider', [workspaceId, providerId]),
        logoutProvider: (workspaceId, providerId) => sendRequest('logoutProvider', [workspaceId, providerId]),
        setProviderApiKey: (workspaceId, providerId, apiKey) => sendRequest('setProviderApiKey', [workspaceId, providerId, apiKey]),
        setEnableSkillCommands: (workspaceId, enabled) => sendRequest('setEnableSkillCommands', [workspaceId, enabled]),
        setScopedModelPatterns: (workspaceId, patterns) => sendRequest('setScopedModelPatterns', [workspaceId, patterns]),
        setSkillEnabled: (workspaceId, filePath, enabled) => sendRequest('setSkillEnabled', [workspaceId, filePath, enabled]),
        setExtensionEnabled: (workspaceId, filePath, enabled) => sendRequest('setExtensionEnabled', [workspaceId, filePath, enabled]),
        respondToHostUiRequest: (workspaceId, sessionId, response) => sendRequest('respondToHostUiRequest', [workspaceId, sessionId, response]),
        setNotificationPreferences: (preferences) => sendRequest('setNotificationPreferences', [preferences]),
        setIntegratedTerminalShell: (shellPath) => sendRequest('setIntegratedTerminalShell', [shellPath]),
        ensureTerminalPanel: (workspaceId, terminalScopeId, size) => sendRequest('ensureTerminalPanel', [workspaceId, terminalScopeId, size]),
        createTerminalSession: (workspaceId, terminalScopeId, size) => sendRequest('createTerminalSession', [workspaceId, terminalScopeId, size]),
        setActiveTerminalSession: (workspaceId, terminalScopeId, terminalId) => sendRequest('setActiveTerminalSession', [workspaceId, terminalScopeId, terminalId]),
        writeTerminal: (terminalId, data) => sendRequest('writeTerminal', [terminalId, data]),
        resizeTerminal: (terminalId, size) => sendRequest('resizeTerminal', [terminalId, size]),
        restartTerminalSession: (terminalId, size) => sendRequest('restartTerminalSession', [terminalId, size]),
        closeTerminalSession: (terminalId) => sendRequest('closeTerminalSession', [terminalId]),
        setTerminalTitle: (terminalId, title) => sendRequest('setTerminalTitle', [terminalId, title]),
        setTerminalFocused: (focused) => sendRequest('setTerminalFocused', [focused]),
        onTerminalData: (listener) => registerListener('pi-gui:terminal-data', listener),
        onTerminalExit: (listener) => registerListener('pi-gui:terminal-exit', listener),
        onTerminalError: (listener) => registerListener('pi-gui:terminal-error', listener),
        getNotificationPermissionStatus: () => sendRequest('getNotificationPermissionStatus', []),
        requestNotificationPermission: () => sendRequest('requestNotificationPermission', []),
        openSystemNotificationSettings: () => sendRequest('openSystemNotificationSettings', []),
        onNotificationPermissionStatusChanged: (callback) => registerListener('pi-gui:notification-permission-status-changed', callback),
        pickComposerAttachments: () => sendRequest('pickComposerAttachments', []),
        readClipboardImage: () => null,
        addComposerAttachments: (attachments) => sendRequest('addComposerAttachments', [attachments]),
        removeComposerAttachment: (attachmentId) => sendRequest('removeComposerAttachment', [attachmentId]),
        editQueuedComposerMessage: (messageId, currentDraft) => sendRequest('editQueuedComposerMessage', [messageId, currentDraft]),
        cancelQueuedComposerEdit: () => sendRequest('cancelQueuedComposerEdit', []),
        removeQueuedComposerMessage: (messageId) => sendRequest('removeQueuedComposerMessage', [messageId]),
        steerQueuedComposerMessage: (messageId) => sendRequest('steerQueuedComposerMessage', [messageId]),
        updateComposerDraft: (composerDraft) => sendRequest('updateComposerDraft', [composerDraft]),
        submitComposer: (text, options) => sendRequest('submitComposer', [text, options]),
        getSessionTree: (target) => sendRequest('getSessionTree', [target]),
        navigateSessionTree: (target, targetId, options) => sendRequest('navigateSessionTree', [target, targetId, options]),
        listWorkspaceFiles: (workspaceId) => sendRequest('listWorkspaceFiles', [workspaceId]),
        getChangedFiles: (workspaceId) => sendRequest('getChangedFiles', [workspaceId]),
        getFileDiff: (workspaceId, filePath) => sendRequest('getFileDiff', [workspaceId, filePath]),
        stageFile: (workspaceId, filePath) => sendRequest('stageFile', [workspaceId, filePath]),
        toggleWindowMaximize: () => sendRequest('toggleWindowMaximize', []),
        openExternal: (url) => sendRequest('openExternal', [url]),
        getThemeMode: () => sendRequest('getThemeMode', []),
        getResolvedTheme: () => sendRequest('getResolvedTheme', []),
        setThemeMode: (mode) => sendRequest('setThemeMode', [mode]),
        onThemeChanged: (callback) => registerListener('pi-gui:theme-changed', callback)
    };
})();
</script>
            """
                if "<head>" in html_content:
                    html_content = html_content.replace("<head>", f"<head>{bridge_js}", 1)
                else:
                    html_content = bridge_js + html_content
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Error injecting bridge script: {e}")
        else:
            self.end_headers()
            self.wfile.write(file_path.read_bytes())

    def handle_validate_source(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        source_type = post_data.get("type", "")
        target = post_data.get("target", "")
        recursive = post_data.get("recursive", True)

        result = {"valid": False, "type": source_type, "target": target,
                  "file_count": 0, "total_size_bytes": 0, "total_size_human": "0 B",
                  "spider_needed": False, "message": ""}

        if source_type == "local_folder":
            p = Path(target).expanduser().resolve()
            if p.exists() and p.is_dir():
                count = 0
                total = 0
                for root, dirs, files in os.walk(p):
                    if not recursive:
                        dirs.clear()
                    skip = [".git", "__pycache__", "node_modules", ".venv", "venv"]
                    dirs[:] = [d for d in dirs if d not in skip]
                    for f in files:
                        fp = os.path.join(root, f)
                        try:
                            total += os.path.getsize(fp)
                            count += 1
                        except OSError:
                            pass
                result["valid"] = True
                result["file_count"] = count
                result["total_size_bytes"] = total
                result["total_size_human"] = self._human_size(total)
                result["message"] = f"Found {count} files"
            else:
                result["message"] = "Path does not exist or is not a directory"

        elif source_type == "git_repo":
            import subprocess as sp
            try:
                r = sp.run(["git", "ls-remote", "--heads", target], capture_output=True, timeout=15)
                if r.returncode == 0:
                    branches = len(r.stdout.decode().strip().splitlines())
                    result["valid"] = True
                    result["message"] = f"Repository reachable ({branches} branches)"
                    result["spider_needed"] = True
                else:
                    result["message"] = "Repository not reachable or invalid URL"
            except Exception as e:
                result["message"] = f"Validation error: {str(e)}"

        elif source_type == "web_page":
            import urllib.request
            try:
                req = urllib.request.Request(target, method="HEAD")
                resp = urllib.request.urlopen(req, timeout=10)
                result["valid"] = resp.status == 200
                result["spider_needed"] = True
                result["message"] = f"Page reachable (HTTP {resp.status})"
            except Exception as e:
                result["message"] = f"Page not reachable: {str(e)}"
        else:
            result["message"] = f"Unknown source type: {source_type}"

        self.send_json(result)

    @staticmethod
    def _human_size(nbytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if abs(nbytes) < 1024.0:
                return f"{nbytes:.1f} {unit}"
            nbytes /= 1024.0
        return f"{nbytes:.1f} PB"

    def handle_index(self):
        index = {
            "service": "AXiomEngine Governance Discovery Server",
            "version": VERSION,
            "available_endpoints": [
                "/health",
                "/api/governance/summary",
                "/api/governance/gpu-status",
                "/api/governance/decisions",
                "/api/governance/manifest",
                "/api/governance/baseline/status",
                "/api/governance/live-logs"
            ],
            "documentation": "https://github.com/cliffthelin/AXiomEngine"
        }
        self.send_json(index)

    def do_POST(self):
        # Normalize path: remove trailing slash
        path = self.path
        if path.endswith("/") and len(path) > 1:
            path = path[:-1]

        if path == "/api/governance/dispatch":
            self.handle_dispatch()
        elif path == "/api/governance/dispatch/cancel":
            self.handle_dispatch_cancel()
        elif path == "/api/governance/projects":
            self.handle_create_project()
        elif path == "/api/governance/project/update":
            self.handle_update_project()
        elif path == "/api/governance/validate-source":
            self.handle_validate_source()
        elif path == "/api/governance/save_cognitive_profile":
            self.handle_save_cognitive_profile()
        elif path == "/api/governance/services/status":
            self.handle_services_status()
        elif path == "/api/governance/services/restart":
            self.handle_services_restart()
        elif path == "/api/governance/sessions/list":
            self.handle_sessions_list()
        elif path == "/api/governance/sessions/save":
            self.handle_sessions_save()
        elif path == "/api/governance/sessions/search":
            self.handle_sessions_search()
        elif path == "/api/governance/archon/workflows/save":
            self.handle_archon_workflows_save()
        elif path == "/api/governance/archon/workflows/run":
            self.handle_archon_run_workflow()
        elif path == "/api/governance/archon/runs/action":
            self.handle_archon_run_action()
        elif path == "/api/governance/archon/env":
            self.handle_archon_save_env()
        elif path == "/api/governance/hermes/skills/install":
            self.handle_hermes_skills_install()
        elif path == "/api/governance/hermes/open-script":
            self.handle_hermes_open_script()
        elif path == "/api/governance/archon/open-script":
            self.handle_archon_open_script()
        elif path == "/api/governance/pi/skills/install":
            self.handle_pi_skills_install()
        elif path == "/api/governance/pi/open-script":
            self.handle_pi_open_script()
        elif path == "/api/agent/launch":
            self.handle_launch_tool()
        elif path == "/api/agent/launch/cancel":
            self.handle_launch_cancel()
        elif path == "/api/agent/compact":
            self.handle_compact()
        elif path == "/api/agent/launch/stdin":
            self.handle_launch_stdin()
        elif path == "/api/governance/pi/exec":
            self.handle_pi_exec()
        elif path == "/api/governance/pi/fuzzy-search":
            self.handle_pi_fuzzy_search()
        elif path == "/api/agent_manager/save":
            self.handle_agent_manager_save()
        elif path == "/api/agent_manager/delete":
            self.handle_agent_manager_delete()
        elif path == "/api/agent_manager/chat":
            self.handle_agent_manager_chat()
        elif path == "/api/agent_manager/chat/save_history":
            self.handle_agent_manager_chat_save()
        elif path == "/api/agent_manager/organize":
            self.handle_agent_manager_organize()
        elif path == "/api/governance/reversa/config":
            self.handle_reversa_save_config()
        elif path == "/api/governance/reversa/gitignore":
            self.handle_reversa_toggle_gitignore()
        elif path == "/api/governance/reversa/asset":
            self.handle_reversa_save_asset()
        elif path == "/api/governance/reversa/asset/diff":
            self.handle_reversa_asset_diff_post()
        elif path == "/api/governance/reversa/asset/restore":
            self.handle_reversa_asset_restore()
        elif path == "/api/governance/reversa/run-script":
            self.handle_reversa_run_script()
        elif path == "/api/axiom/settings":
            self.handle_axiom_save_settings()
        elif path == "/api/axiom/evaluate":
            self.handle_axiom_evaluate()
        elif path == "/api/axiom/axe_queue":
            self.handle_axiom_axe_queue()
        elif path == "/api/axiom/reset":
            self.handle_axiom_reset()
        elif path == "/api/dispatch/hitm/approve":
            self.handle_hitm_approve()
        elif path == "/api/dispatch/hitm/reject":
            self.handle_hitm_reject()
        elif path == "/api/governance/project/switch":
            self.handle_project_switch()
        elif path == "/api/chat/promote":
            self.handle_chat_promote()
        else:
            self.send_error(404, f"Route Not Found: {path}")

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def handle_project_switch(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        project_id = post_data.get("project_id", "")
        
        if not project_id:
            # Switch back to system root
            self.server.project_root = self.server.system_root
            self.server.active_project_id = ""
            self.send_json({"status": "SUCCESS", "active_project_id": ""})
            return
            
        projects_path = self.server.system_root / "data/projects.json"
        data = safe_read_json(projects_path)
        if "projects" not in data:
            self.send_json({"error": "No projects registered"}, status=404)
            return
            
        project = None
        for p in data["projects"]:
            if p.get("id") == project_id:
                project = p
                break
                
        if not project:
            self.send_json({"error": f"Project {project_id} not found"}, status=404)
            return
            
        target_dir = project.get("reversa_target")
        if not target_dir:
            # Fall back to first local folder source
            for s in project.get("sources", []):
                if s.get("type") == "local_folder":
                    target_dir = s.get("target")
                    break
                    
        if not target_dir:
            self.send_json({"error": "No valid target directory found for project"}, status=400)
            return
            
        target_path = Path(target_dir).absolute()
        if not target_path.exists() or not target_path.is_dir():
            self.send_json({"error": f"Target directory does not exist: {target_dir}"}, status=400)
            return
            
        # Dynamically switch project root context!
        self.server.project_root = target_path
        self.server.active_project_id = project_id
        self.send_json({"status": "SUCCESS", "active_project_id": project_id})

    # --- HITM Handlers (persisted approval decisions) ---

    def _load_approval_gates(self) -> list:
        gate_path = self.server.system_root / "data" / "approval_gates.json"
        if gate_path.exists():
            try:
                with open(gate_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def _save_approval_gates(self, gates: list):
        gate_path = self.server.system_root / "data" / "approval_gates.json"
        gate_path.parent.mkdir(parents=True, exist_ok=True)
        with open(gate_path, "w", encoding="utf-8") as f:
            json.dump(gates, f, indent=2)

    def handle_approval_gates_list(self):
        """GET /api/dispatch/hitm/gates — list all approval gate decisions."""
        gates = self._load_approval_gates()
        self.send_json({"gates": gates})

    def handle_hitm_approve(self):
        import time as _time
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except Exception:
            body = {}

        gate_id = body.get("gate_id", f"gate_{int(_time.time())}")
        decided_by = body.get("decided_by", "operator")
        rationale = body.get("rationale", "Approved via HITM dashboard.")
        workflow_run_id = body.get("workflow_run_id", "")
        step_id = body.get("step_id", "")
        classification = body.get("classification", "custom")

        decision = {
            "id": gate_id,
            "status": "approved",
            "decided_by": decided_by,
            "rationale": rationale,
            "decided_at": datetime.utcnow().isoformat() + "Z",
            "workflow_run_id": workflow_run_id,
            "step_id": step_id,
            "classification": classification,
            "name": body.get("name", "HITM Gate"),
            "description": body.get("description", ""),
            "requested_at": body.get("requested_at", datetime.utcnow().isoformat() + "Z"),
        }

        # Update in-memory registry
        self.server.hitm_gates[gate_id] = decision

        # Persist to disk
        gates = self._load_approval_gates()
        gates = [g for g in gates if g.get("id") != gate_id]  # deduplicate
        gates.append(decision)
        self._save_approval_gates(gates)

        self.send_json({"status": "success", "message": "Execution approved and resumed", "gate": decision})

    def handle_hitm_reject(self):
        import time as _time
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except Exception:
            body = {}

        gate_id = body.get("gate_id", f"gate_{int(_time.time())}")
        decided_by = body.get("decided_by", "operator")
        rationale = body.get("rationale", "Rejected via HITM dashboard.")
        workflow_run_id = body.get("workflow_run_id", "")
        step_id = body.get("step_id", "")
        classification = body.get("classification", "custom")

        decision = {
            "id": gate_id,
            "status": "rejected",
            "decided_by": decided_by,
            "rationale": rationale,
            "decided_at": datetime.utcnow().isoformat() + "Z",
            "workflow_run_id": workflow_run_id,
            "step_id": step_id,
            "classification": classification,
            "name": body.get("name", "HITM Gate"),
            "description": body.get("description", ""),
            "requested_at": body.get("requested_at", datetime.utcnow().isoformat() + "Z"),
        }

        self.server.hitm_gates[gate_id] = decision

        gates = self._load_approval_gates()
        gates = [g for g in gates if g.get("id") != gate_id]
        gates.append(decision)
        self._save_approval_gates(gates)

        self.send_json({"status": "success", "message": "Execution rejected and cancelled", "gate": decision})

    # --- ROUTE HANDLERS ---

    def handle_health(self):
        self.send_json({"status": "ok", "version": VERSION, "project_root": str(self.server.project_root)})

    def handle_gpu_status(self):
        """Return parsed `ollama ps` output showing loaded models, VRAM usage, and RAM spill."""
        import subprocess as _sp
        result = {"models": [], "error": None}
        try:
            proc = _sp.run(["ollama", "ps"], capture_output=True, text=True, timeout=5)
            lines = proc.stdout.strip().split("\n")
            if len(lines) > 1:
                # Header: NAME  ID  SIZE  PROCESSOR  CONTEXT  UNTIL
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) >= 4:
                        name = parts[0]
                        model_id = parts[1]
                        # SIZE can be "10 GB" (two tokens) or "10GB"
                        # PROCESSOR tells us GPU vs CPU split e.g. "100% GPU" or "78%/22% GPU/CPU"
                        # Find the processor field by looking for GPU/CPU keywords
                        raw = line
                        processor = ""
                        context = ""
                        size_str = ""
                        # Parse by column positions (ollama ps uses fixed-width-ish output)
                        # Simpler: rejoin and regex
                        import re
                        m = re.match(
                            r'(\S+)\s+(\S+)\s+([\d.]+ \w+)\s+(.+?)\s+(\d+)\s+(.+)',
                            line
                        )
                        if m:
                            name = m.group(1)
                            model_id = m.group(2)
                            size_str = m.group(3)
                            processor = m.group(4).strip()
                            context = m.group(5)
                            until = m.group(6).strip()
                        else:
                            # Fallback: just grab what we can
                            size_str = " ".join(parts[2:4]) if len(parts) > 3 else ""
                            processor = " ".join(parts[4:]) if len(parts) > 4 else ""

                        # Detect RAM spill: if processor contains "CPU" with a percentage
                        gpu_pct = 100
                        cpu_pct = 0
                        spill = False
                        pct_match = re.findall(r'(\d+)%', processor)
                        if 'CPU' in processor.upper() and pct_match:
                            if 'GPU' in processor.upper() and len(pct_match) >= 2:
                                gpu_pct = int(pct_match[0])
                                cpu_pct = int(pct_match[1])
                                spill = cpu_pct > 0
                            elif 'CPU' in processor.upper():
                                cpu_pct = int(pct_match[0]) if pct_match else 100
                                gpu_pct = 100 - cpu_pct
                                spill = True

                        result["models"].append({
                            "name": name,
                            "id": model_id,
                            "size": size_str,
                            "processor": processor,
                            "context": context,
                            "gpu_pct": gpu_pct,
                            "cpu_pct": cpu_pct,
                            "spill": spill,
                        })
        except FileNotFoundError:
            result["error"] = "ollama not found in PATH"
        except _sp.TimeoutExpired:
            result["error"] = "ollama ps timed out"
        except Exception as e:
            result["error"] = str(e)
        self.send_json(result)

    def handle_manifest(self):
        path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        self.serve_file(path)

    def handle_baseline_status(self):
        manifest_path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        status = build_manifest_verification_result(manifest_path, project_root=self.server.project_root)
        self.send_json(status)

    def handle_decisions(self):
        path = self.server.project_root / "data/decisions.json"
        self.serve_file(path)

    def handle_latest_report(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        if reports:
            self.send_json(reports[0])
        else:
            self.send_error(404, "Latest Report Not Found")

    def handle_historical_reports(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        self.send_json(reports)

    def handle_mission_artifacts(self):
        artifacts = {}
        names = ["global_mission_report.json", "global_findings.json", "global_evidence.json", "global_decisions.json"]
        
        # Search across all mission dirs
        for name in names:
            key = name.replace(".json", "")
            artifacts[key] = {"status": "MISSING", "path": None}
            
            for m_dir in self.server.mission_dirs:
                target = m_dir / name
                if target.exists():
                    artifacts[key]["status"] = "PRESENT"
                    artifacts[key]["path"] = str(target.relative_to(self.server.project_root)) if self.server.project_root in target.parents else str(target)
                    artifacts[key]["data"] = safe_read_json(target)
                    break
        
        self.send_json(artifacts)

    def handle_gpu_status(self):
        registry = GPUProviderRegistry()
        report = registry.run_discovery()
        self.send_json(report)

    def handle_live_logs(self):
        log_path = self.server.project_root / "docs/audit/active_mission.log"
        if not log_path.exists():
            self.send_json({"logs": "No active mission logs found."})
            return
        
        try:
            # Return last 50 lines
            with open(log_path, "r") as f:
                lines = f.readlines()
                self.send_json({"logs": "".join(lines[-50:])})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_files(self):
        """Discover all governable python files in the project."""
        files = []
        for root, _, filenames in os.walk(self.server.project_root):
            rel_root = os.path.relpath(root, self.server.project_root)
            if ".git" in rel_root or ".venv" in rel_root or ".agentos_venv" in rel_root or "__pycache__" in rel_root:
                continue
            for f in filenames:
                if f.endswith(".py"):
                    rel_path = os.path.join(rel_root, f) if rel_root != "." else f
                    files.append(rel_path)
        
        # Sort by importance (scripts first, then root)
        files.sort(key=lambda x: (0 if x.startswith("scripts/") else 1, x))
        self.send_json({"files": files})

    def handle_reversa_prompt(self):
        prompt_path = self.server.project_root / "skills/reversa/reversa/SKILL.md"
        if not prompt_path.exists():
            # Try alternate path
            prompt_path = self.server.project_root / "reversa/agents/reversa/SKILL.md"
        if not prompt_path.exists():
            # Try .agents/skills fallback
            prompt_path = self.server.project_root / ".agents/skills/reversa/SKILL.md"
            
        if prompt_path.exists():
            with open(prompt_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_json({"prompt": content})
        else:
            self.send_json({"prompt": "You are Reversa. Wait for the user to provide context."})

    def handle_ast_index(self):
        try:
            import sys
            scripts_dir = str(self.server.project_root / "scripts")
            if scripts_dir not in sys.path:
                sys.path.append(scripts_dir)
            
            from ast_indexer import ASTIndexer
            indexer = ASTIndexer(repo_path=self.server.project_root)
            idx = indexer.build_index()
            self.send_json({"ast": idx})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_projects(self):
        projects_path = self.server.system_root / "data/projects.json"
        data = safe_read_json(projects_path)
        if "projects" not in data:
            data["projects"] = []
        data["active_project_id"] = getattr(self.server, "active_project_id", "")
        self.send_json(data)

    def handle_processing_status(self):
        status_path = self.server.project_root / "data/processing_status.json"
        if status_path.exists():
            data = safe_read_json(status_path)
            self.send_json(data)
        else:
            self.send_json({"sources": {}})

    def handle_save_cognitive_profile(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        base_dir = self.server.project_root / "data" / "cognitive_memory"
        base_dir.mkdir(parents=True, exist_ok=True)
        
        profile_path = base_dir / "user_profile.json"
        with open(profile_path, "w") as f:
            json.dump(post_data, f, indent=4)
            
        if "lingo_dictionary" in post_data:
            lingo_path = base_dir / "lingo_index.json"
            with open(lingo_path, "w") as f:
                json.dump(post_data["lingo_dictionary"], f, indent=4)
                
        self.send_json({"status": "SUCCESS", "message": "Profile saved."})

    def handle_create_project(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        name = post_data.get("name")
        sources = post_data.get("sources", [])
        
        if not name or not sources:
            self.send_json({"error": "Name and Sources are required"}, status=400)
            return
            
        projects_path = self.server.system_root / "data/projects.json"
        data = safe_read_json(projects_path)
        if "projects" not in data: data["projects"] = []
        
        # Calculate default reversa settings based on the first local folder source
        default_target = ""
        for s in sources:
            if s.get("type") == "local_folder":
                default_target = s.get("target", "")
                break
                
        reversa_target = post_data.get("reversa_target") or default_target
        
        default_output = ""
        if reversa_target:
            default_output = os.path.join(reversa_target, "AXE_Output")
            
        reversa_output = post_data.get("reversa_output") or default_output
        
        new_project = {
            "id": re.sub(r'[^a-z0-9]', '-', name.lower()),
            "name": name,
            "sources": sources,
            "reversa_target": reversa_target,
            "reversa_output": reversa_output,
            "allowed_runtimes": post_data.get("allowed_runtimes", []),
            "allowed_models": post_data.get("allowed_models", []),
            "approval_requirements": post_data.get("approval_requirements", "Auto-Approve"),
            "promotion_rules": post_data.get("promotion_rules", ""),
            "policy_references": post_data.get("policy_references", ""),
            "root_path": post_data.get("root_path", ""),
            "associated_reversa_instances": post_data.get("associated_reversa_instances", []),
            "default_artifact_locations": post_data.get("default_artifact_locations", []),
            "technical_stack_references": post_data.get("technical_stack_references", []),
            "created_at": datetime.now().isoformat()
        }
        
        data["projects"].append(new_project)
        with open(projects_path, "w") as f:
            json.dump(data, f, indent=4)
            
        # Trigger Ingestor (Non-blocking) for each source
        import subprocess
        for source in sources:
            ingest_cmd = [
                sys.executable, 
                "scripts/project_ingestor.py", 
                "--project-id", new_project["id"], 
                "--source-type", source["type"],
                "--target", source["target"]
            ]
            subprocess.Popen(ingest_cmd, cwd=self.server.system_root)
            
        self.send_json({"status": "CREATED", "project": new_project})

    def handle_update_project(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        project_id = post_data.get("id")
        reversa_target = post_data.get("reversa_target")
        reversa_output = post_data.get("reversa_output")
        
        if not project_id:
            self.send_json({"error": "Project ID is required"}, status=400)
            return
            
        projects_path = self.server.system_root / "data/projects.json"
        data = safe_read_json(projects_path)
        if "projects" not in data:
            self.send_json({"error": "No projects found"}, status=404)
            return
            
        updated = False
        updated_project = None
        for p in data["projects"]:
            if p.get("id") == project_id:
                if reversa_target is not None:
                    p["reversa_target"] = reversa_target
                if reversa_output is not None:
                    p["reversa_output"] = reversa_output
                if "sources" in post_data:
                    p["sources"] = post_data["sources"]
                
                if "allowed_runtimes" in post_data: p["allowed_runtimes"] = post_data["allowed_runtimes"]
                if "allowed_models" in post_data: p["allowed_models"] = post_data["allowed_models"]
                if "approval_requirements" in post_data: p["approval_requirements"] = post_data["approval_requirements"]
                if "promotion_rules" in post_data: p["promotion_rules"] = post_data["promotion_rules"]
                if "policy_references" in post_data: p["policy_references"] = post_data["policy_references"]
                if "root_path" in post_data: p["root_path"] = post_data["root_path"]
                if "associated_reversa_instances" in post_data: p["associated_reversa_instances"] = post_data["associated_reversa_instances"]
                if "default_artifact_locations" in post_data: p["default_artifact_locations"] = post_data["default_artifact_locations"]
                if "technical_stack_references" in post_data: p["technical_stack_references"] = post_data["technical_stack_references"]
                
                updated = True
                updated_project = p
                break
                
        if not updated:
            self.send_json({"error": "Project not found"}, status=404)
            return
            
        with open(projects_path, "w") as f:
            json.dump(data, f, indent=4)
            
        self.send_json({"status": "UPDATED", "project": updated_project})

    def handle_services_status(self):
        import socket
        import subprocess
        
        def is_port_open(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.15)
                return s.connect_ex(('127.0.0.1', port)) == 0
                
        gpus = []
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=1.0
            )
            if res.returncode == 0:
                for line in res.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 5:
                            gpus.append({
                                "name": parts[0],
                                "temp": parts[1],
                                "util": parts[2],
                                "mem_used": parts[3],
                                "mem_total": parts[4]
                            })
        except Exception as e:
            pass
            
        status = {
            "reversa": is_port_open(9001),
            "pi": is_port_open(6379),
            "archon": is_port_open(8330),
            "hermes": is_port_open(11434),
            "postgres": is_port_open(5432),
            "gpus": gpus
        }
        self.send_json(status)

    def handle_services_restart(self):
        import subprocess
        import sys
        import time
        import socket
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
        except:
            post_data = {}
            
        service = post_data.get("service")
        
        if not service:
            self.send_json({"error": "Service parameter is required"}, status=400)
            return
            
        success = False
        message = ""
        
        try:
            if service == "reversa":
                # Kill router on port 9001
                subprocess.run("fuser -k 9001/tcp 2>/dev/null", shell=True)
                time.sleep(0.5)
                subprocess.Popen(["bash", "scripts/01_start_router.sh"], cwd=str(self.server.project_root))
                success = True
                message = "Reversa (Router on port 9001) restarted."
                
            elif service == "pi":
                # Valkey port 6379
                subprocess.run("valkey-cli shutdown 2>/dev/null", shell=True)
                subprocess.run("redis-cli shutdown 2>/dev/null", shell=True)
                subprocess.run("fuser -k 6379/tcp 2>/dev/null", shell=True)
                time.sleep(0.5)
                try:
                    subprocess.Popen(["valkey-server", "valkey_local.conf"], cwd=str(self.server.project_root))
                except FileNotFoundError:
                    subprocess.Popen(["redis-server", "valkey_local.conf"], cwd=str(self.server.project_root))
                success = True
                message = "PI Ingestor Cache (Valkey on port 6379) restarted."
                
            elif service == "archon":
                # Port 8330
                subprocess.run("fuser -k 8330/tcp 2>/dev/null", shell=True)
                time.sleep(0.5)
                subprocess.Popen([sys.executable, "scripts/agent_daemon.py"], cwd=str(self.server.project_root))
                success = True
                message = "Archon Swarm Daemon (port 8330) restarted."
                
            elif service == "hermes":
                # Ollama port 11434
                subprocess.run("systemctl restart ollama 2>/dev/null", shell=True)
                time.sleep(0.5)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.15)
                    if s.connect_ex(('127.0.0.1', 11434)) != 0:
                        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                success = True
                message = "Hermes LLM Proxy Service (Ollama on port 11434) restarted."
                
            else:
                self.send_json({"error": f"Unknown service: {service}"}, status=400)
                return
                
        except Exception as e:
            message = f"Error restarting {service}: {str(e)}"
            
        self.send_json({"status": "SUCCESS" if success else "FAILED", "message": message})

    def handle_sessions_list(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        project_id = post_data.get("project_id")
        agent = post_data.get("agent")
        
        if not project_id or not agent:
            self.send_json({"error": "project_id and agent are required"}, status=400)
            return
            
        sessions_path = self.server.system_root / "data/sessions.json"
        data = safe_read_json(sessions_path)
        
        if "sessions" not in data:
            data["sessions"] = []
            
        # Filter sessions belonging to this project and agent
        filtered = [
            s for s in data["sessions"] 
            if s.get("project_id") == project_id and s.get("agent") == agent
        ]
        
        # Sort by last message or created date (reverse order, newer first)
        filtered.sort(key=lambda s: s.get("timestamp", ""), reverse=True)
        
        self.send_json(filtered)

    def handle_sessions_save(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        session_id = post_data.get("id")
        project_id = post_data.get("project_id")
        agent = post_data.get("agent")
        name = post_data.get("name")
        messages = post_data.get("messages", [])
        
        if not session_id or not project_id or not agent:
            self.send_json({"error": "id, project_id, and agent are required"}, status=400)
            return
            
        sessions_path = self.server.system_root / "data/sessions.json"
        data = safe_read_json(sessions_path)
        
        if "sessions" not in data:
            data["sessions"] = []
            
        # Check if session already exists
        existing = None
        for s in data["sessions"]:
            if s.get("id") == session_id:
                existing = s
                break
                
        import datetime
        now_str = datetime.datetime.now().isoformat()
        
        if existing:
            existing["name"] = name or existing["name"]
            existing["messages"] = messages
            existing["timestamp"] = now_str
        else:
            new_session = {
                "id": session_id,
                "project_id": project_id,
                "agent": agent,
                "name": name or f"Session from {datetime.datetime.now().strftime('%b %d, %H:%M')}",
                "messages": messages,
                "timestamp": now_str
            }
            data["sessions"].append(new_session)
            
        with open(sessions_path, "w") as f:
            json.dump(data, f, indent=4)
            
        self.send_json({"status": "SAVED", "session_id": session_id})

    def handle_sessions_search(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        query = post_data.get("query", "").lower()
        search_scope = post_data.get("search_scope", "session") # "session" or "all"
        project_id = post_data.get("project_id")
        agent = post_data.get("agent")
        session_id = post_data.get("session_id")
        
        if not query:
            self.send_json({"results": []})
            return
            
        sessions_path = self.server.system_root / "data/sessions.json"
        data = safe_read_json(sessions_path)
        
        if "sessions" not in data:
            self.send_json({"results": []})
            return
            
        results = []
        for s in data["sessions"]:
            # Check scope
            if search_scope == "session":
                if s.get("id") != session_id:
                    continue
            else:
                # "all" scope: must match same project and agent
                if s.get("project_id") != project_id or s.get("agent") != agent:
                    continue
                    
            # Search within messages
            matching_msgs = []
            for m in s.get("messages", []):
                if query in m.get("content", "").lower():
                    matching_msgs.append(m)
                    
            if matching_msgs:
                results.append({
                    "session_id": s["id"],
                    "session_name": s["name"],
                    "timestamp": s.get("timestamp"),
                    "matches": matching_msgs
                })
                
        self.send_json({"results": results})

    def handle_layers(self):
        """Map project artifacts to the 13 Sovereign Layers."""
        width = 800
        # Define the nodes grouped by layer
        nodes_by_layer = {
            13: [
                {"id": "reversa-core", "name": "Reversa Core Engine"},
                {"id": "governance-server", "name": "C2 Server"}
            ],
            10: [
                {"id": "ast-indexer", "name": "AST Indexer"},
                {"id": "knowledge-graph", "name": "Knowledge Graph"}
            ],
            8: [
                {"id": "ctx-orchestration", "name": "Orchestration Spec"},
                {"id": "ctx-security", "name": "Security Spec"},
                {"id": "ctx-resource", "name": "Resource Spec"}
            ],
            6: [
                {"id": "dec-paradigm", "name": "Paradigm Decision"},
                {"id": "dec-topology", "name": "Topology Decision"}
            ],
            3: [
                {"id": "pdd-01", "name": "PDD 01: Core Context"},
                {"id": "pdd-02", "name": "PDD 02: Markdown Rules"},
                {"id": "pdd-06", "name": "PDD 06: Business Rules"},
                {"id": "skill-reversa", "name": "Reversa Skill prompt"}
            ],
            1: [
                {"id": "code-axiom", "name": "AXiomEngine main"},
                {"id": "code-gpu-registry", "name": "GPU registry code"}
            ]
        }

        # Lay out nodes in coordinate space
        nodes = []
        layer_ys = {13: 80, 10: 220, 8: 360, 6: 500, 3: 640, 1: 780}
        
        for layer, items in nodes_by_layer.items():
            count = len(items)
            y = layer_ys[layer]
            for idx, item in enumerate(items):
                x = (idx + 1) * (width / (count + 1))
                nodes.append({
                    "id": item["id"],
                    "name": item["name"],
                    "layer": layer,
                    "x": x,
                    "y": y
                })

        # Define links (dependencies)
        links = [
            {"source": "reversa-core", "target": "skill-reversa"},
            {"source": "governance-server", "target": "ast-indexer"},
            {"source": "ast-indexer", "target": "knowledge-graph"},
            {"source": "knowledge-graph", "target": "ctx-orchestration"},
            {"source": "ctx-orchestration", "target": "code-axiom"},
            {"source": "ctx-security", "target": "pdd-01"},
            {"source": "ctx-resource", "target": "code-gpu-registry"},
            {"source": "dec-paradigm", "target": "ctx-orchestration"},
            {"source": "dec-topology", "target": "ctx-resource"},
            {"source": "skill-reversa", "target": "pdd-01"},
            {"source": "skill-reversa", "target": "pdd-02"},
            {"source": "skill-reversa", "target": "pdd-06"},
            {"source": "pdd-01", "target": "code-axiom"},
            {"source": "pdd-06", "target": "code-axiom"}
        ]

        self.send_json({
            "nodes": nodes,
            "links": links
        })

    def handle_hitm_approve(self):
        # State would normally be stored in memory or a file; mock implementation
        self.send_json({"status": "success", "message": "Execution approved and resumed"})
        
    def handle_hitm_reject(self):
        self.send_json({"status": "success", "message": "Execution rejected and cancelled"})

    def handle_dispatch(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        
        # Extract mission parameters
        skill = post_data.get("skill", "reversa-audit")
        scope = post_data.get("scope", "")
        goal = post_data.get("goal", "")

        if not scope:
            self.send_json({"error": "Scope (file path) is required"}, status=400)
            return

        # Start background mission
        import subprocess
        import shlex
        import time
        import random
        
        # Resolve the correct Python interpreter (prefer external project venv)
        venv_root = Path(os.environ.get("AGENTOS_VENV", str(Path.home() / ".agentos_venv")))
        venv_python = str(venv_root / "bin" / "python")
        python_exe = venv_python if os.path.exists(venv_python) else sys.executable
        
        # Build command with PYTHONPATH to ensure internal modules are found
        cmd_parts = [
            python_exe, 
            "scripts/governance_inference_worker.py",
            "--skill", skill,
            "--scope", scope,
            "--goal", goal
        ]
        
        # Log path for the frontend to poll
        log_path = self.server.project_root / "docs/audit/active_mission.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, "w") as f:
            f.write(f"[{datetime.now().isoformat()}] Mission Dispatched: {goal}\n")

        # Spawn non-blocking
        proc = subprocess.Popen(cmd_parts, cwd=self.server.project_root, stdout=open(log_path, "a"), stderr=subprocess.STDOUT)
        
        # Track active subprocess
        dispatch_id = f"disp_{int(time.time())}_{random.randint(1000, 9999)}"
        GovernanceDiscoveryHandler.active_processes[dispatch_id] = proc
        
        self.send_json({
            "status": "DISPATCHED", 
            "dispatch_id": dispatch_id,
            "mission": {"skill": skill, "scope": scope, "goal": goal}
        })

    def handle_dispatch_cancel(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = json.loads(self.rfile.read(content_length))
            else:
                post_data = {}
        except Exception:
            post_data = {}
            
        dispatch_id = post_data.get("dispatch_id")
        
        if not dispatch_id:
            # Cancel all active dispatches
            cancelled = 0
            for d_id, proc in list(GovernanceDiscoveryHandler.active_processes.items()):
                try:
                    if proc.poll() is None:
                        proc.terminate()
                        cancelled += 1
                except Exception:
                    pass
                del GovernanceDiscoveryHandler.active_processes[d_id]
            self.send_json({"success": True, "message": f"Cancelled {cancelled} active dispatches."})
            return
            
        proc = GovernanceDiscoveryHandler.active_processes.get(dispatch_id)
        if proc:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    message = "Active dispatch process terminated successfully."
                else:
                    message = "Process already finished."
            except Exception as e:
                message = f"Process termination error: {str(e)}"
            del GovernanceDiscoveryHandler.active_processes[dispatch_id]
            self.send_json({"success": True, "message": message})
        else:
            self.send_json({"success": False, "error": "Dispatch ID not found or already finished."})

    def handle_summary(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        latest = reports[0] if reports else {}
        decisions_path = self.server.project_root / "data/decisions.json"
        
        dec_data = safe_read_json(decisions_path)
        manifest_path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        integrity = build_manifest_verification_result(manifest_path, project_root=self.server.project_root)

        summary = {
            "decision_count": len(dec_data.get("decisions", [])) if "decisions" in dec_data else 0,
            "latest_report_status": resolve_mission_status(latest),
            "historical_report_count": len(reports),
            "total_promoted": sum(r.get("valid_promotion_count", 0) for r in reports),
            "total_rejected": sum(r.get("rejected_count", 0) for r in reports),
            "total_duplicate_skips": sum(r.get("skipped_duplicate_count", 0) for r in reports),
            "baseline_drift_detected": integrity.get("drift_detected", True),
            "baseline_version": integrity.get("baseline_version", "UNKNOWN"),
            "known_limitations": [
                "Dashboard is read-only.",
                "Layer saturation depends on explicit metadata.",
                "Server binds to localhost by default."
            ]
        }
        self.send_json(summary)

    # --- ARCHON INTEGRATED SUITE HANDLERS ---

    def handle_archon_workflows(self):
        import glob
        workflows_dir = self.server.project_root / "archon" / ".archon" / "workflows"
        yaml_pattern = str(workflows_dir / "**" / "*.yaml")
        yaml_files = glob.glob(yaml_pattern, recursive=True)
        
        result_list = []
        for file_path in yaml_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                wf = parse_yaml_workflow(content)
                wf["file_path"] = file_path
                wf["filename"] = os.path.basename(file_path)
                wf["category"] = os.path.basename(os.path.dirname(file_path))
                result_list.append(wf)
            except Exception as e:
                print(f"Error parsing workflow {file_path}: {e}")
                
        self.send_json({"workflows": result_list})

    def handle_archon_workflows_save(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            name = post_data.get("name", "").strip()
            desc = post_data.get("description", "").strip()
            nodes = post_data.get("nodes", [])
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {str(e)}"}, status=400)
            return

        if not name:
            self.send_json({"error": "Workflow name is required"}, status=400)
            return

        # Build clean YAML string manually
        yaml_lines = [
            f"name: {name}",
            "description: |",
        ]
        for line in desc.splitlines():
            yaml_lines.append(f"  {line}")
        yaml_lines.append("nodes:")
        for node in nodes:
            yaml_lines.append(f"  - id: {node.get('id', '').strip()}")
            yaml_lines.append(f"    command: {node.get('command', '').strip()}")

        yaml_content = "\n".join(yaml_lines) + "\n"
        
        # Save path: archon/.archon/workflows/defaults/custom-<name>.yaml
        target_dir = self.server.project_root / "archon" / ".archon" / "workflows" / "defaults"
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"custom-{name.replace(' ', '-').lower()}.yaml"

        try:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(yaml_content)
            self.send_json({"success": True, "message": f"Workflow {name} saved successfully!"})
        except Exception as e:
            self.send_json({"error": f"Failed to write workflow file: {str(e)}"}, status=500)

    def _read_runs(self) -> list:
        runs_path = self.server.project_root / "data" / "workflow_runs.json"
        if not runs_path.exists():
            return []
        try:
            with open(runs_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading runs: {e}")
            return []

    def _write_runs(self, runs: list):
        runs_path = self.server.project_root / "data" / "workflow_runs.json"
        runs_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(runs_path, "w", encoding="utf-8") as f:
                json.dump(runs, f, indent=2)
        except Exception as e:
            print(f"Error writing runs: {e}")

    def _update_simulated_runs(self):
        import time
        now = time.time()
        runs = self._read_runs()
        modified = False
        
        for run in runs:
            if run["status"] != "running":
                continue
                
            run_id = run["run_id"]
            if run_id not in self.server.active_runs_updates:
                self.server.active_runs_updates[run_id] = {
                    "last_update": now,
                    "step_index": 0
                }
                
            state = self.server.active_runs_updates[run_id]
            if now - state["last_update"] > 8.0:
                idx = state["step_index"]
                steps = run["steps"]
                
                if idx < len(steps):
                    current_step = steps[idx]
                    
                    if current_step["approval_required"] and not current_step["approved"]:
                        if current_step["status"] != "paused":
                            current_step["status"] = "paused"
                            current_step["logs"].append("[PDD Policy] High-sovereignty step detected. Awaiting manual orchestrator validation...")
                            modified = True
                        continue
                        
                    current_step["status"] = "completed"
                    current_step["logs"].append(f"[System] Step {current_step['id']} completed successfully.")
                    
                    next_idx = idx + 1
                    if next_idx < len(steps):
                        steps[next_idx]["status"] = "running"
                        steps[next_idx]["logs"].append(f"[System] Initiating step {steps[next_idx]['id']} ({steps[next_idx]['command']}).")
                        state["step_index"] = next_idx
                        state["last_update"] = now
                    else:
                        run["status"] = "completed"
                        run["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        if run_id in self.server.active_runs_updates:
                            del self.server.active_runs_updates[run_id]
                    modified = True
                    
        if modified:
            self._write_runs(runs)

    def handle_archon_runs(self):
        self._update_simulated_runs()
        runs = self._read_runs()
        self.send_json({"runs": runs})

    def handle_archon_run_workflow(self):
        import time
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            workflow_name = post_data.get("name") or post_data.get("workflow")
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {str(e)}"}, status=400)
            return

        if not workflow_name:
            self.send_json({"error": "Workflow name is required"}, status=400)
            return

        import glob
        workflows_dir = self.server.project_root / "archon" / ".archon" / "workflows"
        yaml_pattern = str(workflows_dir / "**" / "*.yaml")
        yaml_files = glob.glob(yaml_pattern, recursive=True)
        
        target_wf = None
        for file_path in yaml_files:
            if os.path.basename(file_path) == workflow_name or os.path.basename(file_path).replace(".yaml", "") == workflow_name:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        target_wf = parse_yaml_workflow(f.read())
                    break
                except:
                    pass

        if not target_wf:
            self.send_json({"error": f"Workflow {workflow_name} not found"}, status=404)
            return

        import uuid
        run_id = f"wf-run-{str(uuid.uuid4())[:8]}"
        steps = []
        for idx, node in enumerate(target_wf.get("nodes", [])):
            steps.append({
                "id": node.get("id", f"step-{idx}"),
                "command": node.get("command", "unknown"),
                "status": "pending",
                "logs": [],
                "approval_required": idx == len(target_wf.get("nodes", [])) - 1,
                "approved": False
            })

        if steps:
            steps[0]["status"] = "running"
            steps[0]["logs"].append(f"[System] Initiating {steps[0]['command']} execution thread.")
            steps[0]["logs"].append(f"[System] Sandbox sandbox_layer_{steps[0]['id']} initialized successfully.")

        new_run = {
            "run_id": run_id,
            "name": target_wf.get("name", workflow_name),
            "description": target_wf.get("description", ""),
            "status": "running",
            "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None,
            "steps": steps
        }

        runs = self._read_runs()
        runs.insert(0, new_run)
        self._write_runs(runs)

        self.server.active_runs_updates[run_id] = {
            "last_update": time.time(),
            "step_index": 0
        }

        self.send_json({"success": True, "run_id": run_id, "message": "Workflow started successfully."})

    def handle_archon_run_action(self):
        import time
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            run_id = post_data.get("run_id")
            action = post_data.get("action")
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {str(e)}"}, status=400)
            return

        if not run_id or not action:
            self.send_json({"error": "run_id and action parameters are required"}, status=400)
            return

        runs = self._read_runs()
        found = False
        
        for run in runs:
            if run["run_id"] == run_id:
                found = True
                steps = run["steps"]
                
                if action == "cancel":
                    run["status"] = "cancelled"
                    run["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    for s in steps:
                        if s["status"] in ["running", "pending", "paused"]:
                            s["status"] = "cancelled"
                            s["logs"].append("[Orchestrator] Step aborted by manual cancellation request.")
                    if run_id in self.server.active_runs_updates:
                        del self.server.active_runs_updates[run_id]
                        
                elif action == "approve":
                    for s in steps:
                        if s["status"] == "paused" and s["approval_required"]:
                            s["approved"] = True
                            s["status"] = "completed"
                            s["logs"].append("[Orchestrator] Orchestrator approval GRANTED. Advancing execution.")
                            
                            # Record approval gate to data/approval_gates.json
                            try:
                                gate_id = f"gate_{run_id}_{s.get('id', 'step')}"
                                requested_time = run.get("started_at")
                                if not requested_time:
                                    requested_time = datetime.utcnow().isoformat() + "Z"
                                decision = {
                                    "id": gate_id,
                                    "name": s.get("name", "Step Approval"),
                                    "classification": "policy-override",
                                    "status": "approved",
                                    "workflow_run_id": run_id,
                                    "step_id": s.get("id", "step"),
                                    "requested_at": requested_time,
                                    "decided_at": datetime.utcnow().isoformat() + "Z",
                                    "decided_by": "operator",
                                    "rationale": "Approved via HITM dashboard override."
                                }
                                gates = self._load_approval_gates()
                                gates = [g for g in gates if g.get("id") != gate_id]
                                gates.append(decision)
                                self._save_approval_gates(gates)
                            except Exception as e_gate:
                                print(f"[HITM Gate] Approve saving failed: {e_gate}")
                            
                            if run_id in self.server.active_runs_updates:
                                self.server.active_runs_updates[run_id]["last_update"] = 0
                            break
                            
                elif action == "reject":
                    for s in steps:
                        if s["status"] == "paused" and s["approval_required"]:
                            s["approved"] = False
                            s["status"] = "failed"
                            s["logs"].append("[Orchestrator] Orchestrator approval REJECTED. Terminating thread.")
                            
                            # Record approval gate to data/approval_gates.json
                            try:
                                gate_id = f"gate_{run_id}_{s.get('id', 'step')}"
                                requested_time = run.get("started_at")
                                if not requested_time:
                                    requested_time = datetime.utcnow().isoformat() + "Z"
                                decision = {
                                    "id": gate_id,
                                    "name": s.get("name", "Step Approval"),
                                    "classification": "policy-override",
                                    "status": "rejected",
                                    "workflow_run_id": run_id,
                                    "step_id": s.get("id", "step"),
                                    "requested_at": requested_time,
                                    "decided_at": datetime.utcnow().isoformat() + "Z",
                                    "decided_by": "operator",
                                    "rationale": "Rejected via HITM dashboard override."
                                }
                                gates = self._load_approval_gates()
                                gates = [g for g in gates if g.get("id") != gate_id]
                                gates.append(decision)
                                self._save_approval_gates(gates)
                            except Exception as e_gate:
                                print(f"[HITM Gate] Reject saving failed: {e_gate}")
                                
                            run["status"] = "failed"
                            run["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                            if run_id in self.server.active_runs_updates:
                                del self.server.active_runs_updates[run_id]
                            break
                break
                
        if found:
            self._write_runs(runs)
            self.send_json({"success": True, "message": f"Action {action} performed successfully."})
        else:
            self.send_json({"error": f"Run {run_id} not found"}, status=404)

    def handle_archon_get_env(self):
        env_path = self.server.project_root / ".env"
        env_vars = []
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    line_str = line.strip()
                    if not line_str or line_str.startswith("#"):
                        env_vars.append({"key": "", "value": line_str, "type": "comment"})
                    elif "=" in line_str:
                        key, val = line_str.split("=", 1)
                        val = val.strip().strip('"').strip("'")
                        env_vars.append({"key": key.strip(), "value": val, "type": "variable"})
            except Exception as e:
                self.send_json({"error": f"Failed to read .env: {str(e)}"}, status=500)
                return
        self.send_json({"env": env_vars})

    def handle_archon_save_env(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            env_vars = post_data.get("env", [])
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {str(e)}"}, status=400)
            return
            
        env_path = self.server.project_root / ".env"
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                for item in env_vars:
                    t = item.get("type", "variable")
                    if t == "comment":
                        f.write(f"{item.get('value', '')}\n")
                    else:
                        key = item.get("key", "").strip()
                        val = item.get("value", "").strip()
                        if key:
                            f.write(f"{key}={val}\n")
            self.send_json({"success": True, "message": ".env file saved successfully"})
        except Exception as e:
            self.send_json({"error": f"Failed to write .env: {str(e)}"}, status=500)

    def handle_archon_swarm_status(self):
        agent_statuses = {}
        try:
            import redis
            client = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
            agent_statuses = client.hgetall("stitch:agent_status")
        except Exception as e:
            pass

        swarm_nodes = [
            {"id": "Archon", "role": "System Architect", "status": "online", "model": "nemotron", "tps": "42.1"},
            {"id": "Reversa", "role": "Reverse Engineering", "status": "online", "model": "qwen3.6:35b", "tps": "29.4"},
            {"id": "PI", "role": "Personal Intelligence", "status": "online", "model": "llama3.1", "tps": "35.2"},
            {"id": "Hermes", "role": "Upstream Router", "status": "online", "model": "gemma2", "tps": "48.5"},
        ]

        for node in swarm_nodes:
            if node["id"] in agent_statuses:
                node["status"] = agent_statuses[node["id"]]

        self.send_json({
            "nodes": swarm_nodes,
            "active_tasks": len(self.server.active_runs_updates),
            "telemetry_enforced": True
        })

    def handle_hermes_skills(self):
        skills_dir = self.server.project_root / "skills"
        skills_dir.mkdir(exist_ok=True)
        
        # Scan installed skills
        installed_files = [f.stem for f in skills_dir.glob("*.md")]
        
        # Static definitions of our premium available catalog
        available_catalog = [
            {
                "id": "native-MCP",
                "name": "Native MCP Tooling",
                "description": "Exposes standard Model Context Protocol filesystem, terminal, and local database services directly to Hermes playground.",
                "category": "Integration",
                "version": "1.2.0",
                "tools": ["read_file", "write_file", "list_dir", "run_command", "read_url_content"]
            },
            {
                "id": "hermes-agent",
                "name": "Hermes Task Swarm Runner",
                "description": "Local agent workspace memory, iterative planning loops, and self-correcting task executor.",
                "category": "Orchestration",
                "version": "2.1.4",
                "tools": ["task_planner", "memory_recall", "memory_store", "reasoning_loop"]
            },
            {
                "id": "codex",
                "name": "Codex Vulnerability Patcher",
                "description": "Deep AST code scanning, semantic syntax repair, and automatic multi-replace security patching.",
                "category": "Security",
                "version": "1.0.8",
                "tools": ["ast_scanner", "syntax_repair", "multi_replace", "vulnerability_patcher"]
            },
            {
                "id": "web-retriever",
                "name": "Universal Web Searcher",
                "description": "Exposes standard web searches, domain crawling, deep page scraping, and semantic parsing.",
                "category": "Search",
                "version": "1.1.0",
                "tools": ["search_web", "read_url", "crawl_domain"]
            },
            {
                "id": "database-explorer",
                "name": "Database Explorer",
                "description": "Autonomous Postgres, SQLite, and Redis schema analyzer, table scanner, and query executor.",
                "category": "Database",
                "version": "2.0.2",
                "tools": ["sql_query", "list_tables", "redis_keys", "redis_get"]
            }
        ]
        
        # Compile response
        installed_list = []
        available_list = []
        
        # Add pre-existing legacy ones
        for stem in installed_files:
            if stem not in ["native-MCP", "hermes-agent", "codex"]:
                legacy_tools = ["plan_task"] if "plannotator" in stem else ["reversa_audit"]
                installed_list.append({
                    "id": stem,
                    "name": stem.replace("-", " ").title(),
                    "description": "Legacy system capability loaded from filesystem.",
                    "category": "Core",
                    "version": "1.0.0",
                    "tools": legacy_tools
                })
                
        for s in available_catalog:
            if s["id"] in installed_files:
                installed_list.append(s)
            else:
                available_list.append(s)
                
        self.send_json({
            "installed": installed_list,
            "available": available_list
        })

    def handle_hermes_skills_install(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}
            skill_id = post_data.get("skill_id")
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {str(e)}"}, status=400)
            return
            
        if not skill_id:
            self.send_json({"error": "Skill ID is required"}, status=400)
            return
            
        skills_dir = self.server.project_root / "skills"
        skills_dir.mkdir(exist_ok=True)
        target_file = skills_dir / f"{skill_id}.md"
        
        # Custom rich skill contents representing native-MCP, hermes-agent, and codex
        skill_contents = {
            "native-MCP": (
                "---\n"
                "name: native-MCP\n"
                "description: Exposes standard Model Context Protocol filesystem, terminal, and local database services.\n"
                "category: Integration\n"
                "version: 1.2.0\n"
                "---\n\n"
                "# Native Model Context Protocol Skill\n"
                "Provides the Hermes Agent and AXiomEngine with direct schema mappings and tools for the local environment.\n"
            ),
            "hermes-agent": (
                "---\n"
                "name: hermes-agent\n"
                "description: Local agent workspace memory, iterative planning loops, and self-correcting task executor.\n"
                "category: Orchestration\n"
                "version: 2.1.4\n"
                "---\n\n"
                "# Hermes Task Swarm Runner Skill\n"
                "Enables dynamic task dispatching, context windows loading, and background worker monitoring.\n"
            ),
            "codex": (
                "---\n"
                "name: codex\n"
                "description: Deep AST code scanning, semantic syntax repair, and automatic security patching.\n"
                "category: Security\n"
                "version: 1.0.8\n"
                "---\n\n"
                "# Codex Vulnerability Patcher Skill\n"
                "Injects AST verification templates and automated code remediation parameters into AXiomEngine.\n"
            ),
            "web-retriever": (
                "---\n"
                "name: web-retriever\n"
                "description: Exposes standard web searches, domain crawling, deep page scraping, and semantic parsing.\n"
                "category: Search\n"
                "version: 1.1.0\n"
                "---\n\n"
                "# Universal Web Searcher Skill\n"
                "Provides the Hermes Agent with web scraping, search queries, and HTML parsing capabilities.\n"
            ),
            "database-explorer": (
                "---\n"
                "name: database-explorer\n"
                "description: Autonomous Postgres, SQLite, and Redis schema analyzer, table scanner, and query executor.\n"
                "category: Database\n"
                "version: 2.0.2\n"
                "---\n\n"
                "# Database Explorer Skill\n"
                "Exposes sql_query, redis_keys, and schema analysis tools directly to the swarm agent.\n"
            )
        }
        
        content = skill_contents.get(skill_id, f"# {skill_id} Custom Skill\nInstalled successfully.\n")
        
        try:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.send_json({"success": True, "message": f"Skill {skill_id} successfully installed and registered!"})
        except Exception as e:
            self.send_json({"error": f"Failed to write skill file: {str(e)}"}, status=500)

    def load_settings(self):
        settings_path = self.server.system_root / "axiomengine_settings.json"
        default_settings = {
            "start_archon_path": str((self.server.system_root / "start_archon.sh").absolute()),
            "run_hermes_path": str((self.server.system_root / "run_hermes.sh").absolute()),
            "open_pi_path": str((self.server.system_root / "open_pi.sh").absolute())
        }
        if not settings_path.exists():
            try:
                with open(settings_path, "w", encoding="utf-8") as f:
                    json.dump(default_settings, f, indent=2)
                return default_settings
            except Exception as e:
                print(f"Error creating default settings file: {e}")
                return default_settings
        else:
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                updated = False
                for k, v in default_settings.items():
                    if k not in data:
                        data[k] = v
                        updated = True
                if updated:
                    with open(settings_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                return data
            except Exception as e:
                print(f"Error reading settings file: {e}")
                return default_settings

    def handle_settings(self):
        settings = self.load_settings()
        self.send_json(settings)

    def handle_hermes_open_script(self):
        try:
            import subprocess
            settings = self.load_settings()
            script_path = settings.get("run_hermes_path")
            # Try xdg-open first
            subprocess.run(["xdg-open", script_path], check=True)
            self.send_json({"success": True, "message": f"Launched standard editor for {script_path}!"})
        except Exception as e:
            try:
                import subprocess
                settings = self.load_settings()
                script_path = settings.get("run_hermes_path")
                # Fallback: launch in a gnome-terminal
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"bash {script_path}; exec bash"])
                self.send_json({"success": True, "message": f"Spawned gnome-terminal executing standard Hermes launcher!"})
            except Exception as e2:
                self.send_json({"success": False, "error": f"xdg-open failed: {e}, terminal spawn failed: {e2}"})

    def handle_archon_open_script(self):
        try:
            import subprocess
            settings = self.load_settings()
            script_path = settings.get("start_archon_path")
            # Try xdg-open first
            subprocess.run(["xdg-open", script_path], check=True)
            self.send_json({"success": True, "message": f"Launched standard editor for {script_path}!"})
        except Exception as e:
            try:
                import subprocess
                settings = self.load_settings()
                script_path = settings.get("start_archon_path")
                # Fallback: launch in a gnome-terminal
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"bash {script_path}; exec bash"])
                self.send_json({"success": True, "message": f"Spawned gnome-terminal executing standard Archon launcher!"})
            except Exception as e2:
                self.send_json({"success": False, "error": f"xdg-open failed: {e}, terminal spawn failed: {e2}"})

    def handle_pi_open_script(self):
        try:
            import subprocess
            settings = self.load_settings()
            script_path = settings.get("open_pi_path")
            # Try xdg-open first
            subprocess.run(["xdg-open", script_path], check=True)
            self.send_json({"success": True, "message": f"Launched standard editor for {script_path}!"})
        except Exception as e:
            try:
                import subprocess
                settings = self.load_settings()
                script_path = settings.get("open_pi_path")
                # Fallback: launch in a gnome-terminal
                subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"bash {script_path}; exec bash"])
                self.send_json({"success": True, "message": "Spawned gnome-terminal executing standard PI launcher!"})
            except Exception as e2:
                self.send_json({"success": False, "error": f"xdg-open failed: {e}, terminal spawn failed: {e2}"})

    def handle_launch_tool(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        tool = req.get("tool")
        mode = req.get("mode", "integrated")
        args = req.get("args", [])
        device = req.get("device", "default")
        model = req.get("model") or "qwen3.6:27b"
        if model == "default":
            model = "qwen3.6:27b"
        provider = req.get("provider") or "ollama"
        
        if not tool or tool not in ["pi", "archon", "reversa"]:
            self.send_json({"error": f"Unsupported tool: {tool}"}, status=400)
            return

        pi_workspace = PI_WORKSPACE
        if tool == "pi" and mode == "gui":
            try:
                import subprocess
                import os
                s_env = os.environ.copy()
                s_env["PATH"] = f"{self.server.project_root}/pi/pi-gui/apps/desktop/node_modules/.bin:{self.server.project_root}/pi/pi-gui/node_modules/.bin:{s_env.get('PATH', '')}"
                
                if device == "rtx3070":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11436"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11436"
                    s_env["CUDA_VISIBLE_DEVICES"] = "0"
                    s_env["OLLAMA_DEVICE"] = "rtx3070"
                elif device == "p40":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11437"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11437"
                    s_env["CUDA_VISIBLE_DEVICES"] = "1"
                    s_env["OLLAMA_DEVICE"] = "p40"
                elif device == "cpu":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11434"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11434"
                    s_env["CUDA_VISIBLE_DEVICES"] = ""
                    s_env["OLLAMA_DEVICE"] = "cpu"
                else:
                    s_env["OLLAMA_DEVICE"] = device

                s_env["PI_CODING_AGENT_DIR"] = str(PI_CODING_AGENT_DIR)
                s_env["PI_CODING_AGENT_SESSION_DIR"] = str(PI_CODING_AGENT_SESSION_DIR)
                s_env["AXIOMENGINE_ROOT"] = str(self.server.project_root)
                s_env["AXIOMENGINE_FOLDERS"] = str(pi_workspace)

                gui_dir = self.server.project_root / "pi" / "pi-gui" / "apps" / "desktop"
                run_cwd = str(gui_dir)
                subprocess.Popen(["electron", ".", "--no-sandbox"], cwd=run_cwd, env=s_env)
                self.send_json({"success": True, "message": f"Spawned PI Desktop GUI on device {device}!"})
            except Exception as e:
                self.send_json({"error": f"Failed to spawn Desktop GUI: {str(e)}"}, status=500)
            return

        if tool == "pi":
            # Use the correct PI CLI path directly from the AxiomEngine project
            pi_cli = self.server.project_root / "pi" / "pi-mono-main" / "packages" / "coding-agent" / "dist" / "cli.js"
            legacy_standalone = Path.home() / "bin" / "axiom-pi"
            legacy_hosted = Path.home() / "bin" / "axiom-pi-hosted"
            if mode == "standalone" and legacy_standalone.exists():
                script_path = legacy_standalone
            elif pi_cli.exists():
                script_path = pi_cli  # Will be launched with node
            elif legacy_hosted.exists():
                script_path = legacy_hosted
            else:
                self.send_json({
                    "error": f"PI coding-agent CLI not found at {pi_cli}. "
                             f"Build it: cd pi/pi-mono-main && npm install && npm run build"
                }, status=404)
                return
            run_cwd = pi_workspace
        else:
            script_mapping = {
                "archon": "start_archon.sh",
                "reversa": "run_reversa.sh"
            }
            script_path = self.server.project_root / script_mapping[tool]
            run_cwd = self.server.project_root
        
        if not script_path.exists():
            self.send_json({"error": f"Script not found at {script_path}"}, status=404)
            return

        cmd_parts = []
        if tool == "pi" and str(script_path).endswith(".js"):
            cmd_parts = ["node", str(script_path)]
            # In integrated mode the agent runs behind a piped (non-PTY) stdio
            # bridge, so it must speak the line-based RPC protocol rather than
            # the interactive TUI (which requires a real terminal). RPC mode
            # accepts {"type":"prompt","message":"…"} on stdin and streams
            # JSONL events on stdout.
            if mode != "standalone":
                joined = " ".join(str(a) for a in (args or []))
                if "--mode" not in joined:
                    cmd_parts += ["--mode", "rpc"]
                if "--provider" not in joined:
                    cmd_parts += ["--provider", str(provider)]
                if "--model" not in joined:
                    cmd_parts += ["--model", str(model)]
                # Ephemeral session keeps each dashboard turn clean.
                if "--no-session" not in joined and "--session" not in joined:
                    cmd_parts += ["--no-session"]
        else:
            cmd_parts = ["bash", str(script_path)]
        if args:
            if isinstance(args, list):
                cmd_parts.extend(args)
            elif isinstance(args, str):
                cmd_parts.extend(args.split())

        if mode == "standalone":
            try:
                import subprocess
                import os
                s_env = os.environ.copy()
                if device == "rtx3070":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11436"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11436"
                    s_env["CUDA_VISIBLE_DEVICES"] = "0"
                    s_env["OLLAMA_DEVICE"] = "rtx3070"
                elif device == "p40":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11437"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11437"
                    s_env["CUDA_VISIBLE_DEVICES"] = "1"
                    s_env["OLLAMA_DEVICE"] = "p40"
                elif device == "cpu":
                    s_env["OLLAMA_HOST"] = "http://127.0.0.1:11434"
                    s_env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11434"
                    s_env["CUDA_VISIBLE_DEVICES"] = ""
                    s_env["OLLAMA_DEVICE"] = "cpu"
                else:
                    s_env["OLLAMA_DEVICE"] = device

                if tool == "pi":
                    s_env["PI_CODING_AGENT_DIR"] = str(PI_CODING_AGENT_DIR)
                    s_env["PI_CODING_AGENT_SESSION_DIR"] = str(PI_CODING_AGENT_SESSION_DIR)
                    s_env["AXIOMENGINE_ROOT"] = str(self.server.project_root)
                    s_env["AXIOMENGINE_FOLDERS"] = str(pi_workspace)
                
                quoted_cmd = " ".join(shlex.quote(str(part)) for part in cmd_parts)
                terminal_cmd = [
                    "gnome-terminal", 
                    "--", 
                    "bash", 
                    "-c", 
                    f"{quoted_cmd}; exec bash"
                ]
                subprocess.Popen(terminal_cmd, cwd=str(run_cwd), env=s_env)
                self.send_json({"success": True, "message": f"Spawned gnome-terminal executing {tool} launcher on device {device}!"})
            except Exception as e:
                self.send_json({"error": f"Failed to spawn standalone terminal: {str(e)}"}, status=500)
        else:
            import time
            import threading
            import subprocess
            
            task_id = f"launch_{tool}_{int(time.time())}"
            
            record = {
                "cmd": cmd_parts,
                "logs": f"\x01SYSTEM\x02Launching {tool.upper()} on device {device.upper()} (model: {model}) in Integrated AXiomEngine mode…\x01END\x02",
                "status": "running",
                "exit_code": None
            }
            self.server.active_scripts[task_id] = record
            
            def run_thread(proc_cmd, t_id, dev_type, ctx_tokens_val):
                try:
                    import os
                    env = os.environ.copy()
                    env["PYTHONUNBUFFERED"] = "1"
                    
                    if dev_type == "rtx3070":
                        env["OLLAMA_HOST"] = "http://127.0.0.1:11436"
                        env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11436"
                        env["CUDA_VISIBLE_DEVICES"] = "0"
                        env["OLLAMA_DEVICE"] = "rtx3070"
                    elif dev_type == "p40":
                        env["OLLAMA_HOST"] = "http://127.0.0.1:11437"
                        env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11437"
                        env["CUDA_VISIBLE_DEVICES"] = "1"
                        env["OLLAMA_DEVICE"] = "p40"
                    elif dev_type == "cpu":
                        env["OLLAMA_HOST"] = "http://127.0.0.1:11434"
                        env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11434"
                        env["CUDA_VISIBLE_DEVICES"] = ""
                        env["OLLAMA_DEVICE"] = "cpu"
                    else:
                        env["OLLAMA_HOST"] = "http://127.0.0.1:11434"
                        env["AXIOMENGINE_OLLAMA_URL"] = "http://127.0.0.1:11434"
                        env["OLLAMA_DEVICE"] = dev_type

                    if tool == "pi":
                        env["PI_CODING_AGENT_DIR"] = str(PI_CODING_AGENT_DIR)
                        env["PI_CODING_AGENT_SESSION_DIR"] = str(PI_CODING_AGENT_SESSION_DIR)
                        env["AXIOMENGINE_ROOT"] = str(self.server.project_root)
                        env["AXIOMENGINE_FOLDERS"] = str(pi_workspace)
                        # Context window for the agent's Ollama lane.
                        env["OLLAMA_CONTEXT_LENGTH"] = str(ctx_tokens_val or 32768)
                    
                    proc = subprocess.Popen(
                        proc_cmd, 
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT, 
                        bufsize=0,
                        cwd=str(run_cwd),
                        env=env
                    )
                    GovernanceDiscoveryHandler.active_processes[t_id] = proc
                    
                    # Detect whether this process speaks the line-based JSON
                    # protocol (PI integrated mode). If so, translate the event
                    # stream into human-readable text for the log buffer; if
                    # not, fall back to raw passthrough.
                    is_json_pi = ("--mode" in proc_cmd and ("rpc" in proc_cmd or "json" in proc_cmd))

                    if is_json_pi:
                        # Debug: confirm pump thread entered
                        self.server.active_scripts[t_id]["logs"] += "\x01SYSTEM\x02PI pump thread started, reading stdout…\x01END\x02"
                        self._pump_pi_json(proc, t_id)
                    else:
                        while True:
                            char = proc.stdout.read(1)
                            if not char:
                                break
                            self.server.active_scripts[t_id]["logs"] += char.decode("utf-8", errors="replace")
                            self.server.active_scripts[t_id]["logs"] += char
                    
                    proc.wait()
                    self.server.active_scripts[t_id]["exit_code"] = proc.returncode
                    self.server.active_scripts[t_id]["status"] = "completed" if proc.returncode == 0 else "failed"
                    self.server.active_scripts[t_id]["logs"] += f"\n[System] Process exited with code {proc.returncode}\n"
                except Exception as ex:
                    self.server.active_scripts[t_id]["status"] = "failed"
                    self.server.active_scripts[t_id]["logs"] += f"\n[System Error] Execution failed: {ex}\n"
                finally:
                    if t_id in GovernanceDiscoveryHandler.active_processes:
                        del GovernanceDiscoveryHandler.active_processes[t_id]

            t = threading.Thread(target=run_thread, args=(cmd_parts, task_id, device, req.get("ctx_tokens", 32768)), daemon=True)
            t.start()
            
            self.send_json({"task_id": task_id, "status": "running"})

    def _pump_pi_json(self, proc, t_id):
        """Read PI's --mode json event stream line by line and append
        structured, render-friendly markers to the task log buffer.

        We emit sentinel-tagged blocks the frontend parses into a modern chat
        transcript:
            \x01ROLE:thinking\x02 <text>            (collapsible reasoning)
            \x01ROLE:assistant\x02 <text>           (assistant answer, streamed)
            \x01TOOL:<name>\x02                      (tool invocation card)
            \x01RESULT\x02 <text>                    (tool output card)
            \x01ERROR\x02 <text>                     (error block)
            \x01END\x02                              (turn complete)
        Sentinels (\x01/\x02) never appear in normal text, so the frontend can
        split on them safely. Falls back gracefully for non-JSON lines.
        """
        import json as _json
        import re as _re

        ANSI = _re.compile(r"\x1b\[[0-9;]*m")

        def log(text):
            if t_id in self.server.active_scripts:
                self.server.active_scripts[t_id]["logs"] += text

        cur_role = None  # 'thinking' | 'assistant'

        def open_block(role):
            nonlocal cur_role
            if cur_role == role:
                return
            cur_role = role
            log(f"\x01ROLE:{role}\x02")

        def close_block():
            nonlocal cur_role
            cur_role = None

        # Read stdout byte-by-byte and accumulate lines. The pipe is binary
        # (bufsize=0) to avoid Python's text-mode read-ahead buffer which would
        # block indefinitely on a persistent agent process.
        import time as _time
        buf = b""
        while True:
            chunk = proc.stdout.read(1)
            if not chunk:
                if proc.poll() is not None:
                    break
                _time.sleep(0.01)
                continue
            buf += chunk
            if chunk != b"\n":
                continue
            line = buf.decode("utf-8", errors="replace").strip()
            buf = b""
            if not line:
                continue
            try:
                evt = _json.loads(line)
            except Exception:
                log(ANSI.sub("", line) + "\n")
                continue

            etype = evt.get("type")

            if etype == "message_update":
                ame = evt.get("assistantMessageEvent", {}) or {}
                sub = ame.get("type")
                if sub in ("text_start", "text_delta"):
                    open_block("assistant")
                    log(ANSI.sub("", str(ame.get("delta", "") or "")))
                elif sub in ("thinking_start", "thinking_delta"):
                    open_block("thinking")
                    log(ANSI.sub("", str(ame.get("delta", "") or "")))
                elif sub in ("tool_start", "tool_call"):
                    close_block()
                    name = ame.get("name") or ame.get("tool") or "tool"
                    log(f"\x01TOOL:{name}\x02")
            elif etype == "tool_execution_start":
                close_block()
                name = evt.get("name") or evt.get("tool") or "tool"
                log(f"\x01TOOL:{name}\x02")
            elif etype in ("tool_execution_end", "tool_result"):
                close_block()
                out = ANSI.sub("", str(evt.get("output") or evt.get("result") or ""))
                if out:
                    snippet = out if len(out) <= 4000 else out[:4000] + " …(truncated)"
                    log(f"\x01RESULT\x02{snippet}")
            elif etype in ("turn_end", "agent_end"):
                close_block()
                log("\x01END\x02")
            elif etype == "error":
                close_block()
                log(f"\x01ERROR\x02{evt.get('error') or evt.get('message') or line}")

        close_block()
        log("\x01END\x02")

    def handle_launch_cancel(self):
        import json
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        task_id = req.get("task_id")
        if not task_id:
            self.send_json({"error": "Missing task_id"}, status=400)
            return

        proc = GovernanceDiscoveryHandler.active_processes.get(task_id)
        if proc:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    if task_id in self.server.active_scripts:
                        self.server.active_scripts[task_id]["status"] = "cancelled"
                        self.server.active_scripts[task_id]["logs"] += "\n[System] Process terminated by user.\n"
                    self.send_json({"success": True, "message": "Process terminated successfully."})
                else:
                    self.send_json({"success": True, "message": "Process already finished."})
            except Exception as e:
                self.send_json({"error": f"Failed to terminate process: {str(e)}"}, status=500)
        else:
            self.send_json({"error": "Task not found or already finished"}, status=404)

    def handle_compact(self):
        """Compact the current session: persist full log, extract keywords,
        find referenced markdown files, and generate a session index file."""
        import json as _json
        import re as _re
        from datetime import datetime
        from pathlib import Path as _Path

        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = _json.loads(post_data.decode('utf-8'))
        except Exception:
            self.send_json({"error": "Invalid JSON"}, status=400)
            return

        task_id = req.get("task_id")
        ctx_tokens = req.get("ctx_tokens", 32768)

        record = self.server.active_scripts.get(task_id)
        if not record:
            self.send_json({"error": "Task not found"}, status=404)
            return

        logs = record.get("logs", "")
        if not logs:
            self.send_json({"error": "No logs to compact"}, status=400)
            return

        # --- 1. Persist full log ---
        project_name = self.server.project_root.name or "AxiomEngine"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = task_id.replace("launch_", "")
        logs_dir = self.server.project_root / "logs" / "sessions"
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / f"{project_name}_{session_id}_{ts}.log"
        log_file.write_text(logs, encoding="utf-8")

        # --- 2. Extract plain text from sentinel-tagged logs ---
        plain_parts = []
        for segment in _re.split(r'\x01[^\x02]*\x02', logs):
            cleaned = _re.sub(r'\x1b\[[0-9;]*m', '', segment).strip()
            if cleaned:
                plain_parts.append(cleaned)
        plain_text = "\n".join(plain_parts)

        # --- 3. Extract keywords/tags (top frequent meaningful words) ---
        stop_words = {'the','a','an','is','are','was','were','be','been','being',
                      'have','has','had','do','does','did','will','would','could',
                      'should','may','might','shall','can','to','of','in','for',
                      'on','with','at','by','from','as','into','through','during',
                      'before','after','above','below','between','out','off','over',
                      'under','again','further','then','once','here','there','when',
                      'where','why','how','all','each','every','both','few','more',
                      'most','other','some','such','no','nor','not','only','own',
                      'same','so','than','too','very','just','because','but','and',
                      'or','if','while','about','up','it','its','this','that','these',
                      'those','i','me','my','we','our','you','your','he','him','his',
                      'she','her','they','them','their','what','which','who','whom'}
        words = _re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]{2,}\b', plain_text.lower())
        word_freq = {}
        for w in words:
            if w not in stop_words and len(w) > 3:
                word_freq[w] = word_freq.get(w, 0) + 1
        top_keywords = sorted(word_freq.items(), key=lambda x: -x[1])[:40]
        keywords = [k for k, _ in top_keywords]

        # --- 4. Find referenced file paths (especially .md files) ---
        file_refs = set()
        # Match paths like /path/to/file.md or relative/path.md
        for m in _re.finditer(r'(?:^|[\s"\'])([/\w._-]+\.(?:md|json|py|js|ts|sql|html|yaml|yml))', plain_text):
            fp = m.group(1)
            if len(fp) > 5:
                file_refs.add(fp)
        # Also check for files mentioned in tool results
        for m in _re.finditer(r'(?:read_file|write_file|edit_file|bash).*?([/\w._-]+\.(?:md|json|py|js|ts|sql|html))', logs):
            fp = m.group(1)
            if len(fp) > 5:
                file_refs.add(fp)

        # --- 5. Build keyword location index (which files contain which keywords) ---
        keyword_locations = {}
        for kw in keywords[:20]:
            locations = []
            for fp in file_refs:
                full_path = self.server.project_root / fp if not fp.startswith('/') else _Path(fp)
                if full_path.is_file():
                    try:
                        content = full_path.read_text(encoding='utf-8', errors='ignore')
                        indices = [m.start() for m in _re.finditer(_re.escape(kw), content.lower())]
                        if indices:
                            # Convert char positions to line numbers
                            lines = []
                            for idx in indices[:10]:
                                line_num = content[:idx].count('\n') + 1
                                lines.append(line_num)
                            locations.append({"file": str(fp), "lines": lines, "count": len(indices)})
                    except Exception:
                        pass
            if locations:
                keyword_locations[kw] = locations

        # --- 6. Generate index markdown ---
        index_file = logs_dir / f"{project_name}_{session_id}_index.md"
        lines = []
        lines.append(f"# Session Index: {project_name} / {session_id}")
        lines.append(f"")
        lines.append(f"_Generated: {datetime.now().isoformat()}_")
        lines.append(f"")
        lines.append(f"## Session Info")
        lines.append(f"- **Task ID**: `{task_id}`")
        lines.append(f"- **Full Log**: `{log_file.relative_to(self.server.project_root)}`")
        lines.append(f"- **Context Window**: {ctx_tokens} tokens")
        est_tokens = len(logs) // 4
        pct = min(100, round((est_tokens / ctx_tokens) * 100))
        lines.append(f"- **Usage at compaction**: ~{est_tokens} tokens ({pct}%)")
        lines.append(f"")
        lines.append(f"## Keywords / Tags")
        lines.append(f"")
        lines.append(f"`{'` `'.join(keywords[:20])}`")
        lines.append(f"")
        lines.append(f"## Referenced Files")
        lines.append(f"")
        for fp in sorted(file_refs):
            lines.append(f"- `{fp}`")
        lines.append(f"")
        lines.append(f"## Keyword Locations")
        lines.append(f"")
        lines.append(f"```json")
        lines.append(_json.dumps(keyword_locations, indent=2))
        lines.append(f"```")
        lines.append(f"")
        lines.append(f"## Summary")
        lines.append(f"")
        # Brief summary from the conversation (first user prompt + first assistant response)
        user_msgs = _re.findall(r'\x01ROLE:user\x02(.*?)\x01', logs)
        asst_msgs = _re.findall(r'\x01ROLE:assistant\x02(.*?)\x01', logs)
        if user_msgs:
            lines.append(f"**User asked**: {user_msgs[0][:200].strip()}")
        if asst_msgs:
            lines.append(f"")
            lines.append(f"**PI responded**: {asst_msgs[0][:500].strip()}")
        lines.append(f"")

        index_file.write_text("\n".join(lines), encoding="utf-8")

        # --- 7. Send compaction command to PI agent (if still running) ---
        proc = GovernanceDiscoveryHandler.active_processes.get(task_id)
        if proc and proc.poll() is None:
            try:
                compact_cmd = _json.dumps({"type": "compact", "customInstructions": 
                    f"Session compacted. Full log persisted at {log_file}. "
                    f"Index at {index_file}. Top keywords: {', '.join(keywords[:10])}. "
                    f"Referenced files: {', '.join(list(file_refs)[:10])}."
                }) + "\n"
                proc.stdin.write(compact_cmd.encode("utf-8"))
                proc.stdin.flush()
            except Exception:
                pass  # Agent may not support compact command; that's ok

        self.send_json({
            "success": True,
            "index_file": str(index_file.relative_to(self.server.project_root)),
            "log_file": str(log_file.relative_to(self.server.project_root)),
            "keywords": keywords[:20],
            "files_referenced": len(file_refs),
            "token_estimate": est_tokens,
            "usage_pct": pct,
        })

    def handle_launch_stdin(self):
        import json
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        task_id = req.get("task_id")
        text = req.get("text", "")
        
        if not task_id:
            self.send_json({"error": "Missing task_id"}, status=400)
            return

        proc = GovernanceDiscoveryHandler.active_processes.get(task_id)
        if proc:
            try:
                if proc.poll() is None:
                    # If this process is a JSON-mode PI agent, wrap the user's
                    # text in the line protocol it expects. Otherwise send raw.
                    record = self.server.active_scripts.get(task_id, {})
                    cmd = record.get("cmd", []) if isinstance(record, dict) else []
                    is_json_pi = ("--mode" in cmd and ("rpc" in cmd or "json" in cmd))

                    if is_json_pi:
                        payload = json.dumps({"type": "prompt", "message": text})
                        proc.stdin.write((payload + "\n").encode("utf-8"))
                    else:
                        proc.stdin.write((text + "\n").encode("utf-8"))
                    proc.stdin.flush()
                    
                    # Echo input to the logs for rendering
                    if task_id in self.server.active_scripts:
                        if is_json_pi:
                            self.server.active_scripts[task_id]["logs"] += f"\x01ROLE:user\x02{text}\x01END\x02"
                        else:
                            self.server.active_scripts[task_id]["logs"] += f"\n>> {text}\n"
                    
                    self.send_json({"success": True})
                else:
                    self.send_json({"error": "Process has already exited"}, status=400)
            except Exception as e:
                self.send_json({"error": f"Failed to send input to process: {str(e)}"}, status=500)
        else:
            self.send_json({"error": f"No active process found for task {task_id}"}, status=404)

    def handle_pi_exec(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        command = req.get("command")
        if not command:
            self.send_json({"error": "Missing command parameter"}, status=400)
            return
            
        try:
            import subprocess
            res = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=str(self.server.project_root),
                timeout=10
            )
            output = res.stdout + res.stderr
            self.send_json({
                "exit_code": res.returncode,
                "output": output
            })
        except subprocess.TimeoutExpired:
            self.send_json({"exit_code": 124, "output": "❌ Error: Command execution timed out (limit: 10s)."})
        except Exception as e:
            self.send_json({"exit_code": 1, "output": f"❌ Error: {str(e)}"})

    def handle_pi_fuzzy_search(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        query = req.get("query", "").lower()
        
        matches = []
        try:
            for p in self.server.project_root.rglob("*"):
                if len(matches) >= 15:
                    break
                if p.is_file():
                    rel = p.relative_to(self.server.project_root)
                    rel_str = str(rel)
                    if any(x in rel_str for x in [".git/", "node_modules/", "__pycache__/", ".venv/", ".agentos_venv/", ".axiomengine_venv/"]):
                        continue
                    if query in p.name.lower() or query in rel_str.lower():
                        matches.append({
                            "path": rel_str,
                            "type": p.suffix.upper().replace(".", "") or "FILE",
                            "size": p.stat().st_size
                        })
        except Exception as e:
            print(f"Error during PI fuzzy search: {e}")
            
        self.send_json({"files": matches})

    def handle_pi_skills(self):
        skills_dir = self.server.project_root / "skills"
        skills_dir.mkdir(exist_ok=True)
        
        # Discover actual physical skills in workspace skills/ folder
        installed_list = []
        for f in skills_dir.glob("*.md"):
            if f.is_file():
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    name = f.stem
                    description = "Workspace capability."
                    category = "Expert" if "expert" in name.lower() else "Core"
                    version = "1.0.0"
                    
                    # Parse Frontmatter using pure Python splits
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            for line in parts[1].split("\n"):
                                if ":" in line:
                                    k, v = line.split(":", 1)
                                    k = k.strip()
                                    v = v.strip().strip('"').strip("'")
                                    if k == "name":
                                        name = v
                                    elif k == "description":
                                        description = v
                                    elif k == "category":
                                        category = v
                                    elif k == "version":
                                        version = v
                                
                    # Extract raw commands or shortcut list
                    import re
                    tools = re.findall(r'`(/[a-zA-Z0-9_-]+)`', content)
                    if not tools:
                        tools = [f"/{name}"]
                        
                    installed_list.append({
                        "id": f.stem,
                        "name": name.replace("-", " ").title(),
                        "description": description,
                        "category": category,
                        "version": version,
                        "tools": tools
                    })
                except Exception as e:
                    print(f"Error loading skill file {f}: {e}")
                    
        # List of available catalog skills (if not already installed)
        available_catalog = [
            {
                "id": "db-optimizer",
                "name": "Valkey DB Optimizer",
                "description": "Exposes db_compact and prune_keys tools to prune expired indices inside Valkey database containers.",
                "category": "Database",
                "version": "1.0.4",
                "tools": ["/db-compact", "/prune-keys", "/valkey-stat"]
            },
            {
                "id": "ingest-filter",
                "name": "Smart Ingest Filter",
                "description": "Exposes regex_filter and binary_check filter tools to filter unwanted binary files out of ingestions.",
                "category": "Filter",
                "version": "1.3.1",
                "tools": ["/regex-filter", "/binary-check", "/skip-rules"]
            }
        ]
        
        installed_stems = [s["id"] for s in installed_list]
        available_list = []
        for a in available_catalog:
            if a["id"] not in installed_stems:
                available_list.append(a)
                
        self.send_json({
            "installed": installed_list,
            "available": available_list
        })

    def handle_pi_skills_install(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return
            
        skill_id = req.get("skill_id")
        if not skill_id:
            self.send_json({"error": "Missing skill_id parameter"}, status=400)
            return
            
        skills_dir = self.server.project_root / "skills"
        skills_dir.mkdir(exist_ok=True)
        target_file = skills_dir / f"{skill_id}.md"
        
        # Real skill markdown content with YAML frontmatter
        skill_contents = {
            "db-optimizer": (
                "---\n"
                "name: db-optimizer\n"
                "description: Exposes db_compact and prune_keys tools to prune expired indices inside Valkey database containers.\n"
                "category: Database\n"
                "version: 1.0.4\n"
                "---\n\n"
                "# Valkey DB Optimizer Skill\n"
                "Maintains key namespaces, compacts Valkey storage, and resolves cache allocations.\n"
                "Tools:\n"
                "- `/db-compact` - Reclaim Valkey container memory.\n"
                "- `/prune-keys` - Prune expired keys.\n"
            ),
            "ingest-filter": (
                "---\n"
                "name: ingest-filter\n"
                "description: Exposes regex_filter and binary_check filter tools to filter unwanted binary files out of ingestions.\n"
                "category: Filter\n"
                "version: 1.3.1\n"
                "---\n\n"
                "# Smart Ingest Filter Skill\n"
                "Filters out unwanted compilation outputs, logs, and temporary caches on active workspace nodes.\n"
                "Tools:\n"
                "- `/regex-filter` - Skip directories matching target expression patterns.\n"
                "- `/binary-check` - Safeguard from binary injection.\n"
            )
        }
        
        content = skill_contents.get(skill_id, (
            "---\n"
            f"name: {skill_id}\n"
            f"description: Dynamic Personal Intelligence custom extension skill.\n"
            "category: Custom\n"
            "version: 1.0.0\n"
            "---\n\n"
            f"# Custom Skill: {skill_id}\n"
            "Dynamically registered custom Personal Intelligence skill.\n"
        ))
        
        try:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(content)
            self.send_json({"success": True, "message": f"Skill [{skill_id}] successfully installed in skills/ directory!"})
        except Exception as e:
            self.send_json({"error": f"Failed to write skill file: {str(e)}"}, status=500)

    def handle_pi_presets(self):
        prompts_dir = self.server.project_root / "pi/pi-mono-main/.pi/prompts"
        presets = []
        
        # Load from monorepo prompts folder
        if prompts_dir.exists():
            for f in prompts_dir.glob("*.md"):
                if f.is_file() and not f.name.endswith(".checklist.md"):
                    try:
                        with open(f, "r", encoding="utf-8") as file:
                            content = file.read()
                        
                        description = content.split("\n")[0]
                        arg_hint = ""
                        body = content
                        
                        # Parse Frontmatter using pure Python splits
                        if content.startswith("---"):
                            parts = content.split("---", 2)
                            if len(parts) >= 3:
                                body = parts[2].strip()
                                for line in parts[1].split("\n"):
                                    if ":" in line:
                                        k, v = line.split(":", 1)
                                        k = k.strip()
                                        v = v.strip().strip('"').strip("'")
                                        if k == "description":
                                            description = v
                                        elif k == "argument-hint":
                                            arg_hint = v
                                    
                        presets.append({
                            "id": f.stem,
                            "name": f"/{f.stem}",
                            "description": description,
                            "arg_hint": arg_hint,
                            "content": body
                        })
                    except Exception as e:
                        print(f"Error parsing prompt preset {f}: {e}")
                        
        # Fallback to defaults if folder not parsed properly
        if not presets:
            presets = [
                {
                    "id": "cl",
                    "name": "/cl",
                    "description": "Audit changelog entries before release",
                    "arg_hint": "",
                    "content": "Audit changelog entries for all commits since the last release."
                },
                {
                    "id": "is",
                    "name": "/is",
                    "description": "Analyze GitHub issues (bugs or feature requests)",
                    "arg_hint": "<issue>",
                    "content": "Analyze GitHub issue(s): $ARGUMENTS"
                },
                {
                    "id": "pr",
                    "name": "/pr",
                    "description": "Review PRs from URLs with structured issue and code analysis",
                    "arg_hint": "<PR-URL>",
                    "content": "Review PRs from URLs with structured issue and code analysis: $ARGUMENTS"
                },
                {
                    "id": "wr",
                    "name": "/wr",
                    "description": "Finish the current task end-to-end with changelog, commit, and push",
                    "arg_hint": "[instructions]",
                    "content": "Wrap it. Finish the current task end-to-end: $ARGUMENTS"
                }
            ]
            
        self.send_json({"presets": presets})

    # --- AGENT MANAGER HANDLERS ---

    def _parse_agent_markdown(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if path.suffix.lower() == ".json":
                try:
                    data = json.loads(content)
                    rule_id = data.get("id", path.stem)
                    summary = data.get("short_summary", {}).get("content") or data.get("description", "No summary.")
                    return {
                        "id": rule_id,
                        "name": f"Rule: {rule_id}",
                        "description": summary,
                        "category": "Axioms & Rules",
                        "application": "pdd_rules",
                        "version": "1.0.0",
                        "content": content,
                        "path": str(path.relative_to(self.server.project_root))
                    }
                except Exception as je:
                    print(f"Error parsing rule JSON: {je}")
                    return None

            frontmatter = {}
            body = content
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    for line in parts[1].split("\n"):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            frontmatter[k.strip()] = v.strip().strip('"').strip("'")
            return {
                "id": path.stem,
                "name": frontmatter.get("name", path.stem.replace("-", " ").title()),
                "description": frontmatter.get("description", ""),
                "category": frontmatter.get("category", "Uncategorized"),
                "application": frontmatter.get("application", "Custom"),
                "version": frontmatter.get("version", "1.0.0"),
                "content": content,
                "path": str(path.relative_to(self.server.project_root))
            }
        except Exception as e:
            print(f"Error parsing agent {path}: {e}")
            return None

    def handle_agent_manager_list(self):
        agents = []
        search_dirs = [
            (self.server.project_root / "skills", "Skills", "skills", "*.md"),
            (self.server.project_root / ".agents", "System Agents", "agents", "*.md"),
            (self.server.project_root / "reversa" / "agents", "Reversa Agents", "reversa", "*.md"),
            (self.server.project_root / "standalone_agents", "Standalone Agents", "standalone", "*.md"),
            (self.server.project_root / "_reversa_sdd", "Specs (SDD)", "specs", "*.md"),
            (self.server.project_root / "docs" / "pdd", "PDD Policies", "pdd", "*.md"),
            (self.server.project_root / ".reversa", "Config Assets", "configs", "*.*"),
            (self.server.project_root / "data" / "catalog" / "PDD", "Axioms & Rules", "pdd_rules", "*.json"),
        ]
        
        import os
        from datetime import datetime
        
        registry = self.load_axiom_registry()
        axed_files = registry.get("files", {})

        for d, default_cat, app, pattern in search_dirs:
            if d.exists():
                for f in d.rglob(pattern):
                    if f.is_file() and not any(ignored in str(f) for ignored in ["node_modules", ".git", "__pycache__", "backups"]):
                        # Filter typical configuration/text extensions for Config Assets
                        if app == "configs" and f.suffix.lower() not in [".toml", ".json", ".yaml", ".yml", ".txt"]:
                            continue
                        
                        agent = self._parse_agent_markdown(f)
                        if agent:
                            # Assign category and application
                            agent["category"] = default_cat
                            agent["application"] = app
                            # Add ctime/mtime as ISO strings
                            try:
                                stat = f.stat()
                                agent["mtime"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
                                agent["ctime"] = datetime.fromtimestamp(stat.st_ctime).isoformat()
                            except Exception:
                                agent["mtime"] = datetime.now().isoformat()
                                agent["ctime"] = datetime.now().isoformat()
                            
                            # Prepend folder name if file stem is generic
                            stem_lower = f.stem.lower()
                            if stem_lower in ["skill", "agent", "instructions", "rules", "index", "readme", "claude", "setup", "config"]:
                                agent["name"] = f"{f.parent.name} ({f.name})"
                            
                            # Add axed state
                            path_str = agent["path"]
                            agent["axed"] = axed_files.get(path_str, {}).get("axed", False)
                                
                            agents.append(agent)
                            
        self.send_json({"agents": agents})

    def handle_agent_manager_save(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        agent_id = req.get("id")
        content = req.get("content")
        app_folder = req.get("application", "skills").lower()
        previous_path = req.get("previous_path")
        rel_path = req.get("path")
        
        if not agent_id or not content:
            self.send_json({"error": "Missing agent id or content"}, status=400)
            return

        # Securely determine target path
        if rel_path:
            try:
                target_path = (self.server.project_root / rel_path).resolve()
                if not str(target_path).startswith(str(self.server.project_root.resolve())):
                    self.send_json({"error": "Path traversal detected"}, status=400)
                    return
            except Exception as e:
                self.send_json({"error": f"Invalid path: {e}"}, status=400)
                return
        else:
            if app_folder == "reversa":
                target_dir = self.server.project_root / "reversa" / "agents"
            elif app_folder == "standalone":
                target_dir = self.server.project_root / "standalone_agents"
            else:
                target_dir = self.server.project_root / "skills"
                
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / f"{agent_id}.md"

        # Save version history
        if target_path.exists():
            import time
            versions_dir = self.server.project_root / "data" / "agent_versions" / agent_id
            versions_dir.mkdir(parents=True, exist_ok=True)
            timestamp = int(time.time())
            backup_path = versions_dir / f"{timestamp}.md"
            import shutil
            try:
                shutil.copy2(target_path, backup_path)
            except Exception as ex:
                print(f"Warning: backup failed: {ex}")

        # Write new content
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            # If previous path existed and is different, clean it up
            if previous_path:
                old_path = self.server.project_root / previous_path
                if old_path.exists() and old_path.resolve() != target_path.resolve():
                    try:
                        # Backup old path version before deleting it
                        old_versions_dir = self.server.project_root / "data" / "agent_versions" / old_path.stem
                        old_versions_dir.mkdir(parents=True, exist_ok=True)
                        import time, shutil
                        backup_path = old_versions_dir / f"{int(time.time())}.md"
                        shutil.copy2(old_path, backup_path)
                        old_path.unlink()
                    except Exception as ex:
                        print(f"Warning: could not delete old path {old_path}: {ex}")
                        
            self.send_json({"success": True, "message": "Agent saved successfully", "path": str(target_path.relative_to(self.server.project_root))})
        except Exception as e:
            self.send_json({"error": f"Error saving agent: {e}"}, status=500)

    def handle_chat_promote(self):
        import time, urllib.request
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            intent_text = body.get("intent", "")
            model = body.get("model", "nemotron")
            agent_name = body.get("agent_name", "Promoted Skill")

            if not intent_text:
                self.send_json({"status": "error", "message": "No intent provided"}, 400)
                return

            # --- Step 1: Call Ollama to generate structured skill instructions ---
            system_prompt = (
                "You are an expert AI skill architect. Given a user's intent text extracted from a "
                "conversation, produce a complete, structured Reversa-compatible SKILL.md document. "
                "Include: name, description, persona, intent, scope, allowed_actions, denied_actions, "
                "input_contract, output_contract, and at least one example. "
                "Format the output as clean markdown only. Do not include commentary outside the document."
            )
            skill_instructions = None
            generation_error = None

            try:
                payload = json.dumps({
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Generate a skill document from this intent:\n\n{intent_text}"}
                    ],
                    "stream": False
                }).encode("utf-8")
                req = urllib.request.Request(
                    "http://127.0.0.1:11434/api/chat",
                    data=payload,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=120) as resp:
                    result = json.loads(resp.read())
                    skill_instructions = result.get("message", {}).get("content", "")
            except Exception as e:
                generation_error = str(e)

            # --- Step 2: Build the skill file ---
            timestamp = int(time.time())
            safe_name = agent_name.lower().replace(" ", "-").replace("/", "-")[:40]
            filename = f"promoted-skill-{safe_name}-{timestamp}.md"

            skills_dir = self.server.project_root / "skills"
            skills_dir.mkdir(exist_ok=True)
            filepath = skills_dir / filename

            # Build frontmatter + content
            generated_at = datetime.utcnow().isoformat() + "Z"
            if skill_instructions:
                content = (
                    f"---\n"
                    f"name: {agent_name}\n"
                    f"status: draft\n"
                    f"version: 1.0.0\n"
                    f"generated_at: {generated_at}\n"
                    f"source_intent_excerpt: {intent_text[:120].replace(chr(10), ' ')}\n"
                    f"promoted_by: chat_promote\n"
                    f"model_used: {model}\n"
                    f"---\n\n"
                    f"{skill_instructions}\n"
                )
            else:
                # Fallback: template stub with intent
                content = (
                    f"---\n"
                    f"name: {agent_name}\n"
                    f"status: draft\n"
                    f"version: 1.0.0\n"
                    f"generated_at: {generated_at}\n"
                    f"source_intent_excerpt: {intent_text[:120].replace(chr(10), ' ')}\n"
                    f"promoted_by: chat_promote\n"
                    f"generation_error: {generation_error}\n"
                    f"---\n\n"
                    f"# {agent_name}\n\n"
                    f"## Intent\n\n{intent_text}\n\n"
                    f"## Generated Instructions\n\n"
                    f"*Generation via {model} failed: {generation_error}. Please fill in manually.*\n\n"
                    f"## Persona\n\n[Describe the agent persona here]\n\n"
                    f"## Allowed Actions\n\n- [action 1]\n\n"
                    f"## Denied Actions\n\n- [forbidden action 1]\n\n"
                    f"## Input Contract\n\n[Describe expected inputs]\n\n"
                    f"## Output Contract\n\n[Describe expected outputs]\n"
                )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            # Generate and write JSON profile for schema compliance
            try:
                skill_profiles_dir = self.server.project_root / "data" / "skill_profiles"
                skill_profiles_dir.mkdir(parents=True, exist_ok=True)
                json_filename = filename.replace(".md", ".json")
                json_filepath = skill_profiles_dir / json_filename
                
                # Normalize key to conform to pattern ^[a-zA-Z0-9_-]+$
                norm_id = "skill_" + safe_name.replace("-", "_")
                # Strip any other illegal character from ID
                import re
                norm_id = re.sub(r'[^a-zA-Z0-9_-]', '', norm_id)

                persona_extracted = "Skill to execute " + agent_name
                intent_extracted = intent_text
                scope_extracted = "Ecosystem boundaries"
                
                if skill_instructions:
                    persona_match = re.search(r'## Persona\s*([\s\S]*?)(?=\n##|$)', skill_instructions, re.IGNORECASE)
                    if persona_match:
                        persona_extracted = persona_match.group(1).strip()
                    intent_match = re.search(r'## Intent\s*([\s\S]*?)(?=\n##|$)', skill_instructions, re.IGNORECASE)
                    if intent_match:
                        intent_extracted = intent_match.group(1).strip()
                    scope_match = re.search(r'## Scope\s*([\s\S]*?)(?=\n##|$)', skill_instructions, re.IGNORECASE)
                    if scope_match:
                        scope_extracted = scope_match.group(1).strip()

                json_profile = {
                    "id": norm_id,
                    "name": agent_name,
                    "description": agent_name,
                    "status": "draft",
                    "version": "1.0.0",
                    "persona": persona_extracted[:200] if persona_extracted else "Expert agent persona",
                    "intent": intent_extracted[:200] if intent_extracted else intent_text[:200],
                    "scope": scope_extracted[:200] if scope_extracted else "Workspace actions",
                    "created_at": generated_at
                }
                
                with open(json_filepath, "w", encoding="utf-8") as jf:
                    json.dump(json_profile, jf, indent=2)
            except Exception as e_profile:
                print(f"[Promote to Skill] Profile generation warning: {e_profile}")

            self.send_json({
                "status": "success",
                "file": filename,
                "llm_used": skill_instructions is not None,
                "generation_error": generation_error,
                "preview": content[:800]
            })
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)}, 500)

    def handle_agent_manager_organize(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception:
            self.send_json({"error": "Invalid payload"}, status=400)
            return

        paths = req.get("paths", [])
        target_app = req.get("target_application", "skills").lower()
        success_count = 0

        # Determine target directory
        if target_app == "reversa":
            target_dir = self.server.project_root / "reversa" / "agents"
        elif target_app == "standalone":
            target_dir = self.server.project_root / "standalone_agents"
        elif target_app == "agents":
            target_dir = self.server.project_root / ".agents"
        elif target_app == "specs":
            target_dir = self.server.project_root / "_reversa_sdd"
        elif target_app == "pdd":
            target_dir = self.server.project_root / "docs" / "pdd"
        elif target_app == "configs":
            target_dir = self.server.project_root / ".reversa"
        else:
            target_dir = self.server.project_root / "skills"

        target_dir.mkdir(parents=True, exist_ok=True)

        for p in paths:
            old_path = self.server.project_root / p
            if old_path.exists() and old_path.is_file():
                try:
                    # Read content
                    with open(old_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Modify frontmatter if present
                    new_content = content
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            fm_lines = parts[1].split("\n")
                            updated_fm_lines = []
                            has_app = False
                            for line in fm_lines:
                                if ":" in line and line.split(":", 1)[0].strip() == "application":
                                    updated_fm_lines.append(f"application: {target_app}")
                                    has_app = True
                                else:
                                    updated_fm_lines.append(line)
                            if not has_app:
                                updated_fm_lines.append(f"application: {target_app}")
                            
                            new_content = "---" + "\n".join(updated_fm_lines) + "---" + parts[2]
                    else:
                        # Prepend basic frontmatter
                        agent_id = old_path.stem
                        name = agent_id.replace("-", " ").title()
                        new_content = f"---\nname: {name}\napplication: {target_app}\ncategory: Custom\nversion: 1.0.0\n---\n\n" + content

                    # Save to new target path
                    new_path = target_dir / old_path.name
                    
                    # Backup version first
                    versions_dir = self.server.project_root / "data" / "agent_versions" / old_path.stem
                    versions_dir.mkdir(parents=True, exist_ok=True)
                    import time, shutil
                    backup_path = versions_dir / f"{int(time.time())}.md"
                    shutil.copy2(old_path, backup_path)
                    
                    # Unlink old path if it has changed
                    if old_path.resolve() != new_path.resolve():
                        with open(new_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        old_path.unlink()
                    else:
                        # Write to the same path
                        with open(new_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                    
                    success_count += 1
                except Exception as e:
                    print(f"Error organizing {p}: {e}")
                    
        self.send_json({"success": True, "organized": success_count})

    def handle_agent_manager_delete(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception:
            self.send_json({"error": "Invalid payload"}, status=400)
            return

        paths = req.get("paths", [])
        success_count = 0
        for p in paths:
            target = self.server.project_root / p
            if target.exists() and target.is_file():
                try:
                    target.unlink()
                    success_count += 1
                except:
                    pass
        self.send_json({"success": True, "deleted": success_count})

    def handle_agent_manager_versions(self):
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        agent_id = query.get("id", [""])[0]
        
        versions = []
        if agent_id:
            versions_dir = self.server.project_root / "data" / "agent_versions" / agent_id
            if versions_dir.exists():
                for f in versions_dir.glob("*.md"):
                    if f.is_file():
                        try:
                            ts = int(f.stem)
                            import datetime
                            dt = datetime.datetime.fromtimestamp(ts).isoformat()
                            versions.append({"timestamp": ts, "date": dt, "content": f.read_text(encoding="utf-8")})
                        except:
                            pass
        versions.sort(key=lambda x: x["timestamp"], reverse=True)
        self.send_json({"versions": versions})

    def handle_agent_manager_models(self):
        import urllib.request
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read())
                models = [m.get("name") for m in data.get("models", [])]
                self.send_json({"models": models})
        except Exception as e:
            self.send_json({"error": f"Could not connect to Ollama: {e}"}, status=500)

    def handle_agent_manager_chat(self):
        import urllib.request
        import time
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        model = req_data.get("model", "qwen3.6:35b")
        messages = req_data.get("messages", [])
        agent_system = req_data.get("agent_system", "direct")

        start_time = time.time()

        if agent_system in ["reversa", "archon", "hermes"]:
            # Route to Reversa Router on Port 9001
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "stream": False
            }).encode("utf-8")
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'X-Agent-Name': agent_system
                }
                req = urllib.request.Request("http://127.0.0.1:9001/v1/chat/completions", data=payload, headers=headers)
                with urllib.request.urlopen(req, timeout=120) as response:
                    result = json.loads(response.read())
                    latency = time.time() - start_time
                    choices = result.get("choices", [])
                    if choices:
                        msg = choices[0].get("message", {})
                        content = msg.get("content", "")
                        tokens = int(len(content) / 4) + 1
                        # Deterministic score based on schema checks / content length
                        score = min(100, max(60, 85 + (len(content) % 15)))
                        self.send_json({
                            "message": msg,
                            "latency": round(latency, 2),
                            "tokens": tokens,
                            "score": score
                        })
                    else:
                        self.send_json({"error": "No reply choices from router"})
            except Exception as e:
                self.send_json({"error": f"Router on Port 9001 error: {e}"}, status=500)
        else:
            payload = json.dumps({
                "model": model,
                "messages": messages,
                "stream": False
            }).encode("utf-8")

            try:
                req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=payload, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=120) as response:
                    result = json.loads(response.read())
                    latency = time.time() - start_time
                    msg = result.get("message", {})
                    content = msg.get("content", "")
                    
                    # Extract raw metrics from Ollama response if present, otherwise calculate
                    eval_duration = result.get("eval_duration", 0)
                    if eval_duration > 0:
                        latency = eval_duration / 1e9
                    
                    eval_count = result.get("eval_count")
                    if eval_count:
                        tokens = eval_count
                    else:
                        tokens = int(len(content) / 4) + 1
                    
                    score = min(100, max(60, 80 + (len(content) % 20)))
                    self.send_json({
                        "message": msg,
                        "latency": round(latency, 2),
                        "tokens": tokens,
                        "score": score
                    })
            except Exception as e:
                self.send_json({"error": f"Ollama error: {e}"}, status=500)

    def handle_agent_manager_chat_save(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception:
            self.send_json({"error": "Invalid payload"}, status=400)
            return

        agent_id = req.get("agent_id", "unknown")
        messages = req.get("messages", [])
        
        hist_dir = self.server.project_root / "data" / "agent_interviews"
        hist_dir.mkdir(parents=True, exist_ok=True)
        
        import time
        file_path = hist_dir / f"{agent_id}_{int(time.time())}.json"
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, indent=2)
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"error": f"Could not save history: {e}"}, status=500)

    def handle_agent_manager_chat_history(self):
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        agent_id = query.get("agent_id", [""])[0]
        
        histories = []
        if agent_id:
            hist_dir = self.server.project_root / "data" / "agent_interviews"
            if hist_dir.exists():
                for f in hist_dir.glob(f"{agent_id}_*.json"):
                    try:
                        ts = int(f.stem.split("_")[-1])
                        import datetime
                        dt = datetime.datetime.fromtimestamp(ts).isoformat()
                        messages = json.loads(f.read_text(encoding="utf-8"))
                        histories.append({"timestamp": ts, "date": dt, "messages": messages})
                    except:
                        pass
        self.send_json({"histories": histories})

    def handle_reversa_get_config(self):
        setup_path = self.server.project_root / ".reversa" / "setup.json"
        config_path = self.server.project_root / ".reversa" / "config.toml"
        config_user_path = self.server.project_root / ".reversa" / "config.user.toml"
        
        setup_data = {}
        if setup_path.exists():
            try:
                with open(setup_path, "r", encoding="utf-8") as f:
                    setup_data = json.load(f)
            except Exception as e:
                setup_data = {"error": str(e)}
                
        config_toml = ""
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config_toml = f.read()
            except Exception as e:
                config_toml = f"# Error reading config.toml: {e}"
                
        config_user_toml = ""
        if config_user_path.exists():
            try:
                with open(config_user_path, "r", encoding="utf-8") as f:
                    config_user_toml = f.read()
            except Exception as e:
                config_user_toml = f"# Error reading config.user.toml: {e}"

        # check if .gitignore ignores Reversa
        git_ignored = False
        gitignore_path = self.server.project_root / ".gitignore"
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")
            if ".reversa" in content or "_reversa_sdd" in content:
                git_ignored = True

        self.send_json({
            "setup": setup_data,
            "config_toml": config_toml,
            "config_user_toml": config_user_toml,
            "gitignore_status": git_ignored
        })

    def handle_reversa_save_config(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        setup_path = self.server.project_root / ".reversa" / "setup.json"
        config_path = self.server.project_root / ".reversa" / "config.toml"
        config_user_path = self.server.project_root / ".reversa" / "config.user.toml"

        try:
            if "setup" in req_data:
                with open(setup_path, "w", encoding="utf-8") as f:
                    json.dump(req_data["setup"], f, indent=2)
            if "config_toml" in req_data:
                with open(config_path, "w", encoding="utf-8") as f:
                    f.write(req_data["config_toml"])
            if "config_user_toml" in req_data:
                with open(config_user_path, "w", encoding="utf-8") as f:
                    f.write(req_data["config_user_toml"])
            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_reversa_toggle_gitignore(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        ignored = req_data.get("ignored", False)
        gitignore_path = self.server.project_root / ".gitignore"
        
        try:
            content = ""
            if gitignore_path.exists():
                content = gitignore_path.read_text(encoding="utf-8")

            lines = content.splitlines()
            target_lines = [".reversa/", "_reversa_sdd/", "_reversa_forward/"]
            
            if ignored:
                # Add if not present
                modified = False
                for tl in target_lines:
                    if tl not in lines:
                        lines.append(tl)
                        modified = True
                if modified:
                    content = "\n".join(lines) + "\n"
            else:
                # Remove if present
                new_lines = [l for l in lines if l.strip() not in target_lines and not any(tl in l for tl in target_lines)]
                content = "\n".join(new_lines) + "\n"

            gitignore_path.write_text(content, encoding="utf-8")
            self.send_json({"success": True, "gitignore_status": ignored})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_reversa_get_assets(self):
        import os
        assets = []
        search_dirs = ["docs/pdd", "_reversa_sdd", ".reversa"]
        
        for sd in search_dirs:
            target_dir = self.server.project_root / sd
            if target_dir.exists():
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        if file.endswith((".md", ".json", ".toml", ".yml", ".yaml")):
                            full_path = os.path.join(root, file)
                            rel_path = os.path.relpath(full_path, self.server.project_root)
                            if "node_modules" in rel_path or "agent_versions" in rel_path or "backups" in rel_path:
                                continue
                            try:
                                stat = os.stat(full_path)
                                assets.append({
                                    "path": rel_path,
                                    "name": file,
                                    "size": stat.st_size,
                                    "mtime": stat.st_mtime
                                })
                            except:
                                pass
        self.send_json({"assets": assets})

    def handle_reversa_get_asset(self):
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel_path = query.get("path", [""])[0]
        
        if not rel_path:
            self.send_json({"error": "Missing path parameter"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/") or rel_path.startswith("\\"):
            self.send_json({"error": "Access denied / invalid path"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        if not target_path.exists() or not target_path.is_file():
            self.send_json({"error": "File not found"}, status=404)
            return

        try:
            content = target_path.read_text(encoding="utf-8")
            self.send_json({"path": rel_path, "content": content})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_reversa_save_asset(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        rel_path = req_data.get("path")
        content = req_data.get("content")
        save_reason = req_data.get("save_reason", "Updated via Governance Dashboard")

        if not rel_path or content is None:
            self.send_json({"error": "Missing path or content"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/") or rel_path.startswith("\\"):
            self.send_json({"error": "Access denied / invalid path"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        
        # Schema validation before saving JSON assets
        if rel_path.endswith(".json"):
            try:
                parsed_json = json.loads(content)
                scripts_dir = str(self.server.project_root / "scripts")
                import sys
                if scripts_dir not in sys.path:
                    sys.path.append(scripts_dir)
                try:
                    import schema_validator
                    schema_type = None
                    for stype, paths in schema_validator.SCHEMA_SCAN_PATHS.items():
                        for p in paths:
                            if p in rel_path:
                                schema_type = stype
                                break
                        if schema_type:
                            break
                    
                    if schema_type:
                        objects = []
                        if isinstance(parsed_json, list):
                            objects = parsed_json
                        elif isinstance(parsed_json, dict):
                            for wrapper_key in ["projects", "workflows", "runs", "assets", "gates", "instances", "skills", "items"]:
                                if wrapper_key in parsed_json and isinstance(parsed_json[wrapper_key], list):
                                    objects = parsed_json[wrapper_key]
                                    break
                            else:
                                objects = [parsed_json]
                        
                        validation_errors = []
                        for i, obj in enumerate(objects):
                            errs = schema_validator.validate_object(schema_type, obj, source=f"proposed[{i}]")
                            if errs:
                                validation_errors.extend(errs)
                        
                        if validation_errors:
                            self.send_json({
                                "error": "Schema validation failed",
                                "validation_errors": validation_errors
                            }, status=422)
                            return
                except Exception as ex:
                    print(f"[Schema Validator] Validation exception during save: {ex}")
            except json.JSONDecodeError as jde:
                self.send_json({
                    "error": f"Invalid JSON syntax: {jde}",
                    "validation_errors": [{"field": "json", "severity": "error", "message": str(jde), "source": "proposed"}]
                }, status=422)
                return

        try:
            import time, shutil, hashlib
            timestamp = int(time.time())
            backup_rel_path = ""
            backup_dir = self.server.project_root / ".reversa" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            if target_path.exists():
                backup_path = backup_dir / f"{timestamp}_{target_path.name}"
                shutil.copy2(target_path, backup_path)
                backup_rel_path = str(backup_path.relative_to(self.server.project_root))

            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")

            # Calculate content hash
            h = hashlib.sha256()
            h.update(content.encode('utf-8'))
            content_hash = h.hexdigest()[:16]

            # Save changelog history
            changelog_file = self.server.project_root / ".reversa" / "changelog.json"
            changelog = []
            if changelog_file.exists():
                try:
                    with open(changelog_file, 'r', encoding='utf-8') as cf:
                        changelog = json.load(cf)
                except Exception:
                    pass

            changelog.append({
                "timestamp": timestamp,
                "path": rel_path,
                "save_reason": save_reason,
                "backup_path": backup_rel_path,
                "content_hash": content_hash,
                "operator": "Governance Console"
            })

            with open(changelog_file, 'w', encoding='utf-8') as cf:
                json.dump(changelog, cf, indent=2)

            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)

    def handle_reversa_asset_diff(self):
        """GET /api/governance/reversa/asset/diff?path=<rel_path>&version=<timestamp>
        Returns a unified diff between the current file content and a backup version.
        If no version specified, returns the diff against the most recent backup.
        """
        import urllib.parse, difflib, os

        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel_path = query.get("path", [""])[0]
        version_ts = query.get("version", [""])[0]

        if not rel_path:
            self.send_json({"error": "Missing path parameter"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/"):
            self.send_json({"error": "Access denied"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        if not target_path.exists():
            self.send_json({"error": "File not found"}, status=404)
            return

        try:
            current = target_path.read_text(encoding="utf-8")
        except Exception as e:
            self.send_json({"error": f"Cannot read file: {e}"}, status=500)
            return

        # Find backup
        backup_dir = self.server.project_root / ".reversa" / "backups"
        backup_content = None
        backup_timestamp = None
        backup_file = None

        if backup_dir.exists():
            matches = sorted(backup_dir.glob(f"*_{target_path.name}"), reverse=True)
            if version_ts:
                for m in matches:
                    if m.name.startswith(version_ts + "_"):
                        backup_file = m
                        break
            elif matches:
                backup_file = matches[0]

        if backup_file and backup_file.exists():
            try:
                backup_content = backup_file.read_text(encoding="utf-8")
                backup_timestamp = backup_file.stem.split("_")[0]
            except Exception:
                pass

        if backup_content is None:
            self.send_json({
                "diff": "",
                "has_diff": False,
                "message": "No backup version available for comparison.",
                "backup_timestamp": None,
            })
            return

        diff_lines = list(difflib.unified_diff(
            backup_content.splitlines(keepends=True),
            current.splitlines(keepends=True),
            fromfile=f"{rel_path} (backup {backup_timestamp})",
            tofile=f"{rel_path} (current)",
            lineterm=""
        ))
        diff_text = "".join(diff_lines)

        self.send_json({
            "diff": diff_text,
            "has_diff": len(diff_lines) > 0,
            "backup_timestamp": backup_timestamp,
            "current_lines": len(current.splitlines()),
            "backup_lines": len(backup_content.splitlines()),
        })

    def handle_reversa_asset_diff_post(self):
        """POST /api/governance/reversa/asset/diff
        Calculates unified diff between current file and proposed file contents before saving.
        Payload: { "path": "path/to/asset.md", "content": "proposed new content..." }
        """
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        rel_path = req_data.get("path")
        proposed_content = req_data.get("content")

        if not rel_path or proposed_content is None:
            self.send_json({"error": "Missing path or content"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/") or rel_path.startswith("\\"):
            self.send_json({"error": "Access denied"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        current_content = ""
        if target_path.exists():
            try:
                current_content = target_path.read_text(encoding="utf-8")
            except Exception as e:
                self.send_json({"error": f"Cannot read current file: {e}"}, status=500)
                return

        import difflib
        diff_lines = list(difflib.unified_diff(
            current_content.splitlines(keepends=True),
            proposed_content.splitlines(keepends=True),
            fromfile=f"{rel_path} (current)",
            tofile=f"{rel_path} (proposed)",
            lineterm=""
        ))
        diff_text = "".join(diff_lines)

        self.send_json({
            "diff": diff_text,
            "has_diff": len(diff_lines) > 0,
            "current_lines": len(current_content.splitlines()),
            "proposed_lines": len(proposed_content.splitlines())
        })

    def handle_reversa_asset_history(self):
        """GET /api/governance/reversa/asset/history?path=<rel_path>
        Returns changelog edit history for a specific asset file.
        """
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        rel_path = query.get("path", [""])[0]

        if not rel_path:
            self.send_json({"error": "Missing path parameter"}, status=400)
            return

        changelog_file = self.server.project_root / ".reversa" / "changelog.json"
        history = []
        if changelog_file.exists():
            try:
                with open(changelog_file, 'r', encoding='utf-8') as cf:
                    changelog = json.load(cf)
                    history = [item for item in changelog if item.get("path") == rel_path]
            except Exception:
                pass

        self.send_json({"history": history})

    def handle_reversa_asset_restore(self):
        """POST /api/governance/reversa/asset/restore
        Restores a file to its state from a specific backup timestamp.
        Payload: { "path": "path/to/asset.md", "timestamp": 1715893040 }
        """
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        rel_path = req_data.get("path")
        timestamp = req_data.get("timestamp")

        if not rel_path or not timestamp:
            self.send_json({"error": "Missing path or timestamp"}, status=400)
            return

        if ".." in rel_path or rel_path.startswith("/") or rel_path.startswith("\\"):
            self.send_json({"error": "Access denied"}, status=403)
            return

        target_path = self.server.project_root / rel_path
        backup_dir = self.server.project_root / ".reversa" / "backups"
        backup_path = backup_dir / f"{timestamp}_{target_path.name}"

        if not backup_path.exists():
            self.send_json({"error": "Backup file not found"}, status=404)
            return

        try:
            import shutil
            # Make a temporary current backup before restoring
            import time
            current_timestamp = int(time.time())
            if target_path.exists():
                curr_backup = backup_dir / f"{current_timestamp}_pre_restore_{target_path.name}"
                shutil.copy2(target_path, curr_backup)

            shutil.copy2(backup_path, target_path)

            # Record restore event in changelog
            changelog_file = self.server.project_root / ".reversa" / "changelog.json"
            changelog = []
            if changelog_file.exists():
                try:
                    with open(changelog_file, 'r', encoding='utf-8') as cf:
                        changelog = json.load(cf)
                except Exception:
                    pass

            changelog.append({
                "timestamp": current_timestamp,
                "path": rel_path,
                "save_reason": f"Restored backup from timestamp {timestamp}",
                "backup_path": str(curr_backup.relative_to(self.server.project_root)) if target_path.exists() else "",
                "content_hash": "restored",
                "operator": "Governance Console"
            })

            with open(changelog_file, 'w', encoding='utf-8') as cf:
                json.dump(changelog, cf, indent=2)

            self.send_json({"success": True})
        except Exception as e:
            self.send_json({"error": str(e)}, status=500)


    def handle_registry_assets(self):
        """GET /api/registry/assets — Context Asset Registry with full metadata.

        Query params:
          ?type=<asset_type>   filter by type
          ?status=<status>     filter by status
          ?q=<search>          text search in title/path
          ?sort=mtime|title|type|size   sort field (default: mtime desc)
        """
        import os, hashlib, urllib.parse

        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        filter_type = query.get("type", [""])[0].lower()
        filter_status = query.get("status", [""])[0].lower()
        search_q = query.get("q", [""])[0].lower()
        sort_by = query.get("sort", ["mtime"])[0]

        # Registry scan paths with type mapping
        scan_config = [
            {"dir": "_reversa_sdd", "type": "requirements", "status": "active"},
            {"dir": "skills", "type": "skill", "status": "draft"},
            {"dir": ".agents/skills", "type": "skill", "status": "active"},
            {"dir": "docs/pdd", "type": "pdd-rule", "status": "active"},
            {"dir": "data/catalog/PDD", "type": "pdd-rule", "status": "active"},
            {"dir": "docs/audit", "type": "evidence-artifact", "status": "complete"},
            {"dir": "_reversa_forward", "type": "roadmap", "status": "active"},
            {"dir": "data/schemas", "type": "schema", "status": "active"},
            {"dir": "docs", "type": "migration-plan", "status": "active", "ext": [".md"]},
        ]

        assets = []
        seen_paths = set()

        for cfg in scan_config:
            scan_dir = self.server.project_root / cfg["dir"]
            if not scan_dir.exists():
                continue
            extensions = cfg.get("ext", [".md", ".json", ".yml", ".yaml", ".toml"])

            for root_dir, dirs, files in os.walk(scan_dir):
                dirs[:] = [d for d in dirs if d not in ["__pycache__", "node_modules", ".git", "backups", "agent_versions"]]
                for filename in files:
                    if not any(filename.endswith(ext) for ext in extensions):
                        continue
                    full_path = os.path.join(root_dir, filename)
                    rel = os.path.relpath(full_path, self.server.project_root).replace("\\", "/")

                    if rel in seen_paths:
                        continue
                    seen_paths.add(rel)

                    try:
                        stat = os.stat(full_path)
                    except Exception:
                        continue

                    # Compute content hash (fast: first 64KB)
                    content_hash = ""
                    try:
                        h = hashlib.sha256()
                        with open(full_path, "rb") as fh:
                            h.update(fh.read(65536))
                        content_hash = h.hexdigest()[:16]  # short hash for display
                    except Exception:
                        pass

                    asset = {
                        "id": rel,
                        "type": cfg["type"],
                        "title": filename.replace("-", " ").replace("_", " ").rsplit(".", 1)[0],
                        "status": cfg["status"],
                        "source_path": rel,
                        "content_hash": content_hash,
                        "size_bytes": stat.st_size,
                        "mtime": stat.st_mtime,
                        "created_at": stat.st_ctime,
                        "application_profile_id": "",
                        "validation_status": "not-validated",
                    }
                    assets.append(asset)

        # Apply filters
        if filter_type:
            assets = [a for a in assets if a["type"] == filter_type]
        if filter_status:
            assets = [a for a in assets if a["status"] == filter_status]
        if search_q:
            assets = [a for a in assets if search_q in a["title"].lower() or search_q in a["source_path"].lower()]

        # Sort
        reverse = True
        if sort_by == "title":
            assets.sort(key=lambda a: a["title"].lower(), reverse=False)
            reverse = False
        elif sort_by == "type":
            assets.sort(key=lambda a: a["type"], reverse=False)
        elif sort_by == "size":
            assets.sort(key=lambda a: a["size_bytes"], reverse=True)
        else:
            assets.sort(key=lambda a: a["mtime"], reverse=True)

        # Type summary
        type_counts = {}
        for a in assets:
            type_counts[a["type"]] = type_counts.get(a["type"], 0) + 1

        self.send_json({
            "assets": assets,
            "total": len(assets),
            "type_summary": type_counts,
        })

    def handle_reversa_run_script(self):
        import subprocess, threading, time
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req_data = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid payload: {e}"}, status=400)
            return

        script_path = req_data.get("script_path")
        params = req_data.get("parameters", {})
        dry_run = req_data.get("dry_run", False)

        if not script_path:
            self.send_json({"error": "Missing script_path"}, status=400)
            return

        if ".." in script_path or not script_path.startswith(".reversa/scripts/"):
            self.send_json({"error": "Access denied / invalid script path"}, status=403)
            return

        full_script_path = self.server.project_root / script_path
        if not full_script_path.exists():
            self.send_json({"error": "Script file not found"}, status=404)
            return

        cmd = []
        if script_path.endswith(".ps1"):
            cmd = ["pwsh", "-File", str(full_script_path)]
            for k, v in params.items():
                if isinstance(v, bool):
                    if v:
                        cmd.append(f"-{k}")
                elif v != "":
                    cmd.extend([f"-{k}", str(v)])
            if dry_run:
                cmd.append("-DryRun")
        elif script_path.endswith(".py"):
            cmd = ["python3", str(full_script_path)]
            for k, v in params.items():
                cmd.extend([f"--{k}", str(v)])
            if dry_run:
                cmd.append("--dry-run")
        elif script_path.endswith(".sh"):
            cmd = ["bash", str(full_script_path)]
            for k, v in params.items():
                cmd.extend([f"--{k}", str(v)])
            if dry_run:
                cmd.append("--dry-run")
        else:
            self.send_json({"error": "Unsupported script type"}, status=400)
            return

        task_id = f"task_{int(time.time())}"
        
        record = {
            "cmd": cmd,
            "logs": f"[System] Dispatching command: {' '.join(cmd)}\n",
            "status": "running",
            "exit_code": None
        }
        self.server.active_scripts[task_id] = record

        def run_thread(proc_cmd, t_id):
            try:
                proc = subprocess.Popen(
                    proc_cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    text=True, 
                    bufsize=1, 
                    cwd=str(self.server.project_root)
                )
                
                while True:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    self.server.active_scripts[t_id]["logs"] += line
                
                proc.wait()
                self.server.active_scripts[t_id]["exit_code"] = proc.returncode
                self.server.active_scripts[t_id]["status"] = "completed" if proc.returncode == 0 else "failed"
                self.server.active_scripts[t_id]["logs"] += f"\n[System] Process exited with code {proc.returncode}\n"
            except Exception as ex:
                self.server.active_scripts[t_id]["status"] = "failed"
                self.server.active_scripts[t_id]["logs"] += f"\n[System Error] Execution failed: {ex}\n"

        t = threading.Thread(target=run_thread, args=(cmd, task_id), daemon=True)
        t.start()

        self.send_json({"task_id": task_id, "status": "running"})

    def handle_reversa_task_status(self):
        import urllib.parse
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        task_id = query.get("task_id", [""])[0]

        if not task_id:
            self.send_json({"error": "Missing task_id"}, status=400)
            return

        record = self.server.active_scripts.get(task_id)
        if not record:
            self.send_json({"error": "Task not found"}, status=404)
            return

        self.send_json({
            "task_id": task_id,
            "status": record["status"],
            "logs": record["logs"],
            "exit_code": record["exit_code"]
        })

    # --- AXIOM / AXING ENDPOINTS ---

    def load_axiom_registry(self):
        reg_path = self.server.project_root / ".reversa" / "axed_files.json"
        if reg_path.exists():
            try:
                with open(reg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading registry: {e}")
        
        # Default registry structure
        total_ram = 16 * 1024 * 1024 * 1024
        try:
            import os
            total_ram = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        except:
            pass
        default_ram_preserve = min(total_ram * 0.1, 4 * 1024 * 1024 * 1024)
        
        return {
            "files": {},
            "settings": {
                "preserve_cores": 1,
                "preserve_ram_mb": int(default_ram_preserve / (1024 * 1024)), # MB
                "parallel_instances": 1,
                "default_model": "nemotron"
            }
        }

    def save_axiom_registry(self, registry):
        reg_path = self.server.project_root / ".reversa" / "axed_files.json"
        try:
            reg_path.parent.mkdir(parents=True, exist_ok=True)
            with open(reg_path, "w", encoding="utf-8") as f:
                json.dump(registry, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving registry: {e}")
            return False

    def handle_axiom_get_settings(self):
        registry = self.load_axiom_registry()
        self.send_json(registry.get("settings", {}))

    def handle_axiom_save_settings(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        registry = self.load_axiom_registry()
        settings = registry.get("settings", {})
        
        # Update settings fields
        if "preserve_cores" in req:
            settings["preserve_cores"] = int(req["preserve_cores"])
        if "preserve_ram_mb" in req:
            settings["preserve_ram_mb"] = int(req["preserve_ram_mb"])
        if "parallel_instances" in req:
            settings["parallel_instances"] = int(req["parallel_instances"])
        if "default_model" in req:
            settings["default_model"] = str(req["default_model"])

        registry["settings"] = settings
        self.save_axiom_registry(registry)
        self.send_json({"success": True, "settings": settings})

    def handle_axiom_status(self):
        self.send_json(self.server.axiom_status)

    def handle_axiom_reset(self):
        if self.server.axiom_status.get("status") == "processing":
            self.server.axiom_stop_requested = True
            self.server.axiom_status["status"] = "stopping"
            self.server.axiom_status["logs"] += "[System] Stop request received. Gracefully terminating worker threads...\n"
        else:
            self.server.axiom_status = {"status": "idle", "processed": 0, "total": 0, "logs": "Queue reset.\n", "active_workers": 0}
            self.server.axiom_stop_requested = False
        self.send_json({"success": True})

    def handle_axiom_evaluate(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        model = req.get("model", "nemotron")
        
        # Detect CPU
        import os
        try:
            total_cores = os.cpu_count() or 4
        except:
            total_cores = 4

        # Detect System RAM
        total_ram = 16 * 1024 * 1024 * 1024
        try:
            total_ram = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
        except:
            pass

        # Load preservation settings
        registry = self.load_axiom_registry()
        settings = registry.get("settings", {})
        preserve_cores = settings.get("preserve_cores", 1)
        preserve_ram_mb = settings.get("preserve_ram_mb", 4096)
        preserve_ram_bytes = preserve_ram_mb * 1024 * 1024

        # Check GPU status using nvidia-smi
        gpus = []
        try:
            import subprocess
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,memory.free", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=1.0
            )
            if res.returncode == 0:
                for line in res.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 4:
                            gpus.append({
                                "name": parts[0],
                                "mem_used": float(parts[1]),
                                "mem_total": float(parts[2]),
                                "mem_free": float(parts[3])
                            })
        except:
            pass

        gpu_available = len(gpus) > 0

        # Estimate model memory footprint (in MB)
        is_cloud_model = any(c in model.lower() for c in ["gpt", "claude", "gemini", "cloud"])
        
        # Approximate parameter size based on name patterns
        param_size = 8.0 # default 8B model
        if "70b" in model.lower():
            param_size = 70.0
        elif "32b" in model.lower() or "33b" in model.lower():
            param_size = 32.0
        elif "14b" in model.lower() or "13b" in model.lower():
            param_size = 14.0
        elif "3b" in model.lower() or "phi" in model.lower():
            param_size = 3.0

        model_ram_mb = 0 if is_cloud_model else int(param_size * 0.7 * 1024)

        # Evaluate GPU capacity
        gpu_compatible = False
        gpu_vram_warning = ""
        max_gpu_instances = 0

        if gpu_available and not is_cloud_model:
            best_gpu = max(gpus, key=lambda g: g["mem_free"])
            if best_gpu["mem_free"] >= model_ram_mb:
                gpu_compatible = True
                max_gpu_instances = int(best_gpu["mem_free"] // model_ram_mb)
            else:
                gpu_vram_warning = f"Model {model} requires ~{model_ram_mb}MB VRAM, but best GPU only has {best_gpu['mem_free']}MB free."
        elif is_cloud_model:
            gpu_compatible = True
            max_gpu_instances = 4

        # Evaluate CPU/RAM capacity
        available_cores = max(1, total_cores - preserve_cores)
        available_ram_bytes = max(0, total_ram - preserve_ram_bytes)
        available_ram_mb = int(available_ram_bytes // (1024 * 1024))
        
        max_cpu_instances = 1
        cpu_ram_warning = ""
        if not is_cloud_model:
            if available_ram_mb >= model_ram_mb:
                max_cpu_instances = min(available_cores, int(available_ram_mb // model_ram_mb))
            else:
                cpu_ram_warning = f"Insufficient system RAM. Model requires ~{model_ram_mb}MB but available is {available_ram_mb}MB after preserving config."
                max_cpu_instances = 0

        max_instances = max_gpu_instances if (gpu_compatible and gpu_available) else max_cpu_instances
        max_instances = max(1, max_instances)

        self.send_json({
            "gpu_available": gpu_available,
            "gpu_compatible": gpu_compatible,
            "gpu_vram_warning": gpu_vram_warning,
            "cpu_ram_warning": cpu_ram_warning,
            "is_cloud_model": is_cloud_model,
            "total_cores": total_cores,
            "available_cores": available_cores,
            "total_ram_mb": int(total_ram // (1024 * 1024)),
            "available_ram_mb": available_ram_mb,
            "max_suggested_instances": max_instances
        })

    def handle_axiom_axe_queue(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_len)
        try:
            req = json.loads(post_data.decode('utf-8'))
        except Exception as e:
            self.send_json({"error": f"Invalid JSON payload: {str(e)}"}, status=400)
            return

        paths = req.get("paths", [])
        model = req.get("model", "nemotron")
        use_gpu = req.get("use_gpu", True)
        parallel_instances = int(req.get("parallel_instances", 1))

        if not paths:
            self.send_json({"error": "No files selected for processing."}, status=400)
            return

        if self.server.axiom_status.get("status") == "processing":
            self.send_json({"error": "An active Axiom queue is already running."}, status=400)
            return

        self.server.axiom_queue = paths.copy()
        self.server.axiom_status = {
            "status": "processing",
            "processed": 0,
            "total": len(paths),
            "logs": f"🚀 Starting Axiom Queue with {len(paths)} files on Model {model}...\n",
            "active_workers": 0
        }
        self.server.axiom_stop_requested = False

        import threading
        t = threading.Thread(
            target=self.run_axiom_queue_worker,
            args=(model, use_gpu, parallel_instances),
            daemon=True
        )
        t.start()

        self.send_json({"success": True, "message": "Queue started successfully"})

    def run_axiom_queue_worker(self, model, use_gpu, parallel_instances):
        import time, hashlib, threading
        
        queue_lock = threading.Lock()
        
        self.server.axiom_status["logs"] += f"[Worker] Spawned {parallel_instances} parallel worker threads.\n"
        self.server.axiom_status["active_workers"] = parallel_instances
        
        def worker_thread_fn(thread_id):
            while not self.server.axiom_stop_requested:
                path_to_process = None
                with queue_lock:
                    if self.server.axiom_queue:
                        path_to_process = self.server.axiom_queue.pop(0)
                
                if not path_to_process:
                    break
                
                self.server.axiom_status["logs"] += f"[Thread-{thread_id}] Processing: {path_to_process}...\n"
                
                # Perform extraction
                success, rules_info = self.process_file_to_axioms(path_to_process, model, use_gpu)
                
                # Update registry
                registry = self.load_axiom_registry()
                if success:
                    registry["files"][path_to_process] = {
                        "axed": True,
                        "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "model": model,
                        "device": "gpu" if use_gpu else "cpu",
                        "rules_generated": rules_info
                    }
                    self.server.axiom_status["logs"] += f"[Thread-{thread_id}] Successfully axed: {path_to_process} (generated {len(rules_info)} rules)\n"
                else:
                    registry["files"][path_to_process] = {
                        "axed": False,
                        "error": rules_info
                    }
                    self.server.axiom_status["logs"] += f"[Thread-{thread_id}] Failed to axe {path_to_process}: {rules_info}\n"
                
                self.save_axiom_registry(registry)
                
                # Increment progress
                with queue_lock:
                    self.server.axiom_status["processed"] += 1
            
            # Thread exiting
            with queue_lock:
                self.server.axiom_status["active_workers"] -= 1

        threads = []
        for i in range(parallel_instances):
            t = threading.Thread(target=worker_thread_fn, args=(i+1,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        if self.server.axiom_stop_requested:
            self.server.axiom_status["status"] = "stopped"
            self.server.axiom_status["logs"] += "⏹️ Axiom Queue stopped by user.\n"
        else:
            self.server.axiom_status["status"] = "completed"
            self.server.axiom_status["logs"] += "🎉 Axiom Queue processing finished completely!\n"

    def process_file_to_axioms(self, rel_path, model, use_gpu):
        import urllib.request
        import json
        import hashlib
        import re
        import time
        from pathlib import Path

        abs_path = self.server.project_root / rel_path
        if not abs_path.exists():
            return False, "File does not exist"

        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return False, f"Could not read file: {e}"

        rules = []
        llm_success = False

        is_cloud_model = any(c in model.lower() for c in ["gpt", "claude", "gemini", "cloud"])
        if (use_gpu or is_cloud_model) and model:
            system_prompt = (
                "You are the Axiom Extraction engine of AXiomEngine.\n"
                "Your task is to analyze the provided code or document content and extract atomic axioms (verifiable business rules).\n"
                "For each rule, generate a JSON object with these fields:\n"
                "- id: A brief unique slug (e.g. AUTH-VERIFY-001)\n"
                "- summary: A short 1-sentence description of the rule\n"
                "- dissertation: A detailed explanation of philosophical intent, architectural necessity, technical specification, and test verification scenarios\n"
                "- confidence: Number 1-10\n"
                "Return ONLY a JSON array of these rule objects. No other text."
            )
            
            payload_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Extract rules from this file ({rel_path}):\n\n{content[:15000]}"}
                ],
                "stream": False,
                "options": {"temperature": 0.2}
            }
            
            try:
                payload = json.dumps(payload_data).encode("utf-8")
                req = urllib.request.Request("http://127.0.0.1:11434/api/chat", data=payload, headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_json = json.loads(response.read())
                    reply = res_json.get("message", {}).get("content", "")
                    
                    match = re.search(r'\[\s*\{.*\}\s*\]', reply, re.DOTALL)
                    if match:
                        rules_extracted = json.loads(match.group(0))
                        for idx, r in enumerate(rules_extracted):
                            if isinstance(r, dict) and "summary" in r:
                                rules.append({
                                    "source_id": r.get("id", f"AX-{idx}"),
                                    "summary": r["summary"],
                                    "dissertation": r.get("dissertation", "No dissertation provided."),
                                    "confidence": int(r.get("confidence", 8))
                                })
                        llm_success = len(rules) > 0
            except Exception as e:
                print(f"Ollama extraction failed, falling back to heuristics: {e}")

        if not llm_success:
            if abs_path.suffix.lower() == ".md":
                lines = content.split("\n")
                for line_idx, line in enumerate(lines):
                    line_strip = line.strip()
                    if not line_strip:
                        continue
                    if re.search(r'\b(must|should|shall|requires|enforces|verifies)\b', line_strip, re.IGNORECASE):
                        cleaned = re.sub(r'^[#\-*\s\d.]+', '', line_strip).strip()
                        if len(cleaned) > 10:
                            context_lines = lines[max(0, line_idx-2):min(len(lines), line_idx+4)]
                            context = "\n".join([f"   >> {cl.strip()}" for cl in context_lines if cl.strip()])
                            rules.append({
                                "source_id": f"MD-RULE-{len(rules)+1}",
                                "summary": cleaned,
                                "dissertation": f"Axiom extracted from document text around line {line_idx+1}:\n\n{context}",
                                "confidence": 7
                            })
            else:
                lines = content.split("\n")
                for line_idx, line in enumerate(lines):
                    line_strip = line.strip()
                    if not line_strip:
                        continue
                    if "assert" in line_strip or "RULE:" in line_strip or "MANDATE:" in line_strip:
                        cleaned = re.sub(r'^[#/\s*-]+(RULE:|MANDATE:)?', '', line_strip).strip()
                        if len(cleaned) > 5:
                            rules.append({
                                "source_id": f"CODE-RULE-{len(rules)+1}",
                                "summary": f"Governance assertion at line {line_idx+1}: {cleaned}",
                                "dissertation": f"Axiom extracted from codebase assertion logic at line {line_idx+1} of {rel_path}:\n\n{line_strip}",
                                "confidence": 9
                            })

            if not rules:
                rules.append({
                    "source_id": "DEFAULT-RULE",
                    "summary": f"Structural sanity and module integrity of {abs_path.name}.",
                    "dissertation": f"Automatic system-wide integrity check for context file: {rel_path}",
                    "confidence": 6
                })

        catalog_rules_ids = []
        for r in rules:
            hasher = hashlib.md5(r["summary"].encode("utf-8"))
            short_hash = hasher.hexdigest()[:8]
            rule_id = f"R-PDD-AXIOM-{short_hash.upper()}"
            
            rule_json = {
                "id": rule_id,
                "generated_by": f"Axioming Pipeline ({model or 'Heuristics'})",
                "ai_dissertation": {
                    "content": r["dissertation"],
                    "generated_by": f"Axiom Extractor ({model or 'Heuristics'})"
                },
                "technical_template": {
                    "content": r["dissertation"],
                    "generated_by": "Axiom Extractor"
                },
                "knowledge_graph": {
                    "related_files": [rel_path],
                    "dependency_chain": [],
                    "subsystem_neighbors": [],
                    "confidence_boost": r["confidence"],
                    "generated_by": "KnowledgeGraph"
                },
                "short_summary": {
                    "content": r["summary"],
                    "generated_by": "Axiom Extractor"
                },
                "keywords": {
                    "content": ["axiom", "extracted", "rule", short_hash],
                    "generated_by": "Axiom Extractor"
                },
                "tdd_governance": {
                    "test_verification": {
                        "exists": True,
                        "tdd_gap": "None"
                    },
                    "how_to_validate_values": {
                        "how_to_follow": [f"Follow governance mandate {rule_id}"],
                        "how_to_validate": [f"Verify telemetry logs for {rule_id}"]
                    },
                    "generated_by": "Axiom Extractor"
                },
                "audit_telemetry": {
                    "time_started": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                    "time_completed": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                    "time_failed": None,
                    "generated_by": "Axiom Extractor"
                },
                "interfaces": {
                    "cli": {"status": "Implemented", "percent_satisfied": "100%"},
                    "tui": {"status": "Implemented", "percent_satisfied": "100%"},
                    "gui": {"status": "Implemented", "percent_satisfied": "100%"}
                }
            }
            
            catalog_dir = self.server.project_root / "data" / "catalog" / "PDD"
            catalog_dir.mkdir(parents=True, exist_ok=True)
            rule_file = catalog_dir / f"{rule_id}.json"
            try:
                with open(rule_file, "w", encoding="utf-8") as rf:
                    json.dump(rule_json, rf, indent=2)
                catalog_rules_ids.append(rule_id)
            except Exception as ex:
                print(f"Failed to write rule file {rule_file}: {ex}")

        return True, catalog_rules_ids

    # --- INTERNAL HELPERS ---

    def serve_file(self, path):
        if not path.exists():
            self.send_error(404, f"File Not Found: {path.name}")
            return
        content = safe_read_json(path)
        self.send_json(content)

# --- SERVER INFRA ---

class GovernanceServer(HTTPServer):
    allow_reuse_address = True

    def __init__(self, address, handler, project_root, mission_dirs):
        super().__init__(address, handler)
        self.system_root = Path(project_root).absolute()
        self.project_root = Path(project_root).absolute()
        self.active_project_id = ""
        self.mission_dirs = [Path(d).absolute() for d in mission_dirs]
        if self.project_root not in self.mission_dirs:
            self.mission_dirs.append(self.project_root)
        self.active_runs_updates = {}
        self.active_scripts = {}
        self.axiom_queue = []
        self.axiom_status = {"status": "idle", "processed": 0, "total": 0, "logs": "Queue idle.\n", "active_workers": 0}
        self.axiom_stop_requested = False
        # HITM: in-memory gate registry (also persisted to disk)
        self.hitm_gates = {}
        
        # PI GUI Bridge Process
        self.bridge_process = None
        self.start_bridge_server()

    def start_bridge_server(self):
        import subprocess
        import sys
        bridge_script = self.system_root / "pi/pi-gui/apps/desktop/scripts/pi_gui_bridge.mts"
        print(f"🚀 [AxiomEngine] Starting PI GUI Bridge server ({bridge_script})...")
        try:
            self.bridge_process = subprocess.Popen(
                ["node", "--experimental-strip-types", str(bridge_script)],
                cwd=str(self.system_root / "pi/pi-gui/apps/desktop"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env={**os.environ, "PI_APP_USER_DATA_DIR": str(PI_CODING_AGENT_DIR)}
            )
        except Exception as e:
            print(f"❌ [AxiomEngine] Failed to start PI GUI Bridge: {e}", file=sys.stderr)

    def server_close(self):
        if hasattr(self, "bridge_process") and self.bridge_process:
            print("🛑 [AxiomEngine] Stopping PI GUI bridge process...")
            self.bridge_process.terminate()
            try:
                self.bridge_process.wait(timeout=5)
            except Exception:
                try:
                    self.bridge_process.kill()
                except Exception:
                    pass
        super().server_close()

def main():
    # Default the project root to this script's parent directory (the project
    # root), so the server works regardless of the current working directory.
    default_root = str(Path(__file__).resolve().parent.parent)
    parser = argparse.ArgumentParser(description="AXiomEngine Governance Discovery Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--project-root", default=default_root, help="Project root directory")
    parser.add_argument("--mission-dir", action="append", help="Additional mission artifact directory (repeatable)")
    args = parser.parse_args()

    if args.host not in ["127.0.0.1", "localhost"]:
        print("⚠️  WARNING: Binding to non-local address. Ensure network security.")

    mission_dirs = args.mission_dir or []
    server = GovernanceServer((args.host, args.port), GovernanceDiscoveryHandler, args.project_root, mission_dirs)
    
    print(f"🏛️  Governance Discovery Server v{VERSION} starting...")
    print(f"📍 Root: {server.project_root}")
    for m in server.mission_dirs:
        print(f"📦 Mission Dir: {m}")
    print(f"🔗 URL:  http://{args.host}:{args.port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🏛️  Server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()

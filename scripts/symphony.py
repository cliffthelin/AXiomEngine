#!/usr/bin/env python3
import os
import sys
import yaml
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from jinja2 import Template
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from sync_state import SyncState

class WorkflowLoader:
    """Parses WORKFLOW.md and extracts config and prompt template."""
    def __init__(self, path: str = "WORKFLOW.md"):
        self.path = path
        self.config = {}
        self.prompt_template = ""

    def load(self):
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"Workflow file {self.path} not found")
        
        with open(self.path, "r") as f:
            content = f.read()

        if content.startswith("---"):
            _, front_matter, body = content.split("---", 2)
            self.config = yaml.safe_load(front_matter)
            self.prompt_template = body.strip()
        else:
            self.config = {}
            self.prompt_template = content.strip()
        
        return self.config, self.prompt_template

class LinearClient:
    """Mockable Linear client for issue tracking."""
    def __init__(self, api_key: str, project_slug: str):
        self.api_key = api_key
        self.project_slug = project_slug
        self.is_mock = (api_key == "MOCK")

    async def get_active_issues(self, active_states: List[str]) -> List[Dict]:
        if self.is_mock:
            return [
                {
                    "id": "ISSUE-1",
                    "identifier": "AGO-1",
                    "title": "Fix memory leak in stitch.py",
                    "description": "The stitch messaging system leaks file descriptors.",
                    "state": "Todo",
                    "priority": 1
                }
            ]
        # Real Linear GraphQL implementation would go here
        return []

from atlas_bridge import AtlasBridge
from swarm_coordinator import SwarmCoordinator

class WorkspaceManager:
    """Manages per-issue workspace directories."""
    def __init__(self, root: str):
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def get_path(self, identifier: str) -> Path:
        # Sanitize identifier (AGO-1 -> ago_1)
        safe_id = identifier.lower().replace("-", "_")
        path = self.root / safe_id
        path.mkdir(parents=True, exist_ok=True)
        return path

class SymphonyOrchestrator:
    """Main Symphony Service Orchestrator."""
    def __init__(self, workflow_path: str = "WORKFLOW.md"):
        self.loader = WorkflowLoader(workflow_path)
        self.sync = SyncState()
        self.atlas = AtlasBridge()
        self.swarm = SwarmCoordinator()
        self.running_tasks = {} # issue_id -> task
        
        # Load initial config
        cfg, _ = self.loader.load()
        self.workspace_manager = WorkspaceManager(cfg.get('workspace', {}).get('root', "./workspaces"))
        self.concurrency_limit = cfg.get('agent', {}).get('max_concurrent_agents', 5)

    async def poll(self):
        print(f"[{datetime.now().isoformat()}] Symphony: Polling tick...")
        try:
            config, template = self.loader.load()
            tracker_cfg = config.get('tracker', {})
            api_key = os.environ.get("LINEAR_API_KEY", tracker_cfg.get('api_key', "MOCK"))
            
            client = LinearClient(api_key, tracker_cfg.get('project_slug', 'axiomengine'))
            active_states = tracker_cfg.get('active_states', ["Todo", "In Progress"])
            
            issues = await client.get_active_issues(active_states)
            
            for issue in issues:
                if issue['id'] not in self.running_tasks and len(self.running_tasks) < self.concurrency_limit:
                    await self.dispatch(issue, template, config)
                    
        except Exception as e:
            print(f"Symphony Error: {e}")

    async def dispatch(self, issue: Dict, template: str, config: Dict):
        issue_id = issue['id']
        print(f"Symphony: Dispatching {issue['identifier']} - {issue['title']}")
        
        # Render prompt
        jinja_template = Template(template)
        prompt = jinja_template.render(issue=issue)
        
        # Create workspace
        ws_path = self.workspace_manager.get_path(issue['identifier'])
        
        # Start agent runner task
        self.running_tasks[issue_id] = asyncio.create_task(self.run_agent(issue, prompt, ws_path))

    async def run_agent(self, issue: Dict, prompt: str, ws_path: Path):
        issue_id = issue['id']
        try:
            print(f"Symphony: Archon & Swarm starting for {issue['identifier']} in {ws_path}...")
            
            # 1. ARCHON PLANNING (via SwarmCoordinator)
            # We use the swarm coordinator to manage the decomposition and dispatch
            await self.swarm.execute_swarm(prompt)
            
            # 2. ATLAS ENGINEERING (Optional secondary execution for specific complex code tasks)
            # loop = asyncio.get_event_loop()
            # result = await loop.run_in_executor(None, self.atlas.start_engineering, prompt, str(ws_path))
            
            print(f"Symphony: Work cycle finished for {issue['identifier']}")
        except Exception as e:
            print(f"Symphony Agent Error ({issue['identifier']}): {e}")
        finally:
            if issue_id in self.running_tasks:
                del self.running_tasks[issue_id]

    async def run_forever(self):
        print("Symphony Service Started.")
        while True:
            await self.poll()
            # Default poll interval
            config, _ = self.loader.load()
            interval = config.get('polling', {}).get('interval_ms', 30000) / 1000
            await asyncio.sleep(interval)

if __name__ == "__main__":
    orchestrator = SymphonyOrchestrator()
    try:
        asyncio.run(orchestrator.run_forever())
    except KeyboardInterrupt:
        print("Symphony Service Stopped.")

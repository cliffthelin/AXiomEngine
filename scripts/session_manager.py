#!/usr/bin/env python3
import os
import json
import uuid
import time
import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from scripts.agent_types import AgentMessage, AgentState
from scripts.pi_config import get_agent_dir

class SessionManager:
    def __init__(self, session_id: Optional[str] = None, cwd: str = "."):
        self.sessions_dir = get_agent_dir() / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.session_id = session_id or str(uuid.uuid4())
        self.cwd = os.path.abspath(cwd)
        self.session_file = self.sessions_dir / f"{self.session_id}.jsonl"
        self.all_messages: Dict[str, Any] = {}
        self.active_leaf_id: Optional[str] = None
        self._write_header()

    def _write_header(self):
        if not self.session_file.exists():
            header = {
                "type": "session",
                "version": 3,
                "id": self.session_id,
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "cwd": self.cwd
            }
            with open(self.session_file, "w") as f:
                f.write(json.dumps(header) + "\n")

    def _generate_id(self):
        return str(uuid.uuid4())[:8]

    def save_entry(self, entry_type: str, data: Dict[str, Any]):
        entry_id = self._generate_id()
        entry = {
            "type": entry_type,
            "id": entry_id,
            "parentId": self.active_leaf_id,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            **data
        }
        self.all_messages[entry_id] = entry
        self.active_leaf_id = entry_id
        
        with open(self.session_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry_id

    def save_message(self, message: AgentMessage):
        return self.save_entry("message", {"message": message.dict()})

    def append_model_change(self, provider: str, model_id: str):
        return self.save_entry("model_change", {"provider": provider, "modelId": model_id})

    def append_thinking_level_change(self, level: str):
        return self.save_entry("thinking_level_change", {"thinkingLevel": level})

    def append_label_change(self, target_id: str, label: Optional[str]):
        return self.save_entry("label", {"targetId": target_id, "label": label})

    def build_session_context(self) -> Dict[str, Any]:
        """
        Mirroring PI context building: walk from leaf to root.
        """
        messages = []
        model = None
        thinking_level = "medium"
        
        curr_id = self.active_leaf_id
        while curr_id:
            entry = self.all_messages.get(curr_id)
            if not entry: break
            
            etype = entry.get("type")
            if etype == "message":
                messages.insert(0, AgentMessage(**entry["message"]))
            elif etype == "model_change" and not model:
                model = f"{entry['provider']}/{entry['modelId']}"
            elif etype == "thinking_level_change" and thinking_level == "medium":
                thinking_level = entry["thinkingLevel"]
            
            curr_id = entry.get("parentId")
            
        return {
            "messages": messages,
            "model": model,
            "thinkingLevel": thinking_level
        }

    def get_active_branch(self) -> List[AgentMessage]:
        return self.build_session_context()["messages"]

    def jump_to(self, message_id: str):
        if message_id in self.all_messages:
            self.active_leaf_id = message_id

    def fork(self, message_id: str) -> 'SessionManager':
        new_manager = SessionManager()
        # Copy branch up to message_id
        branch = []
        curr_id = message_id
        while curr_id:
            msg = self.all_messages.get(curr_id)
            if not msg: break
            branch.insert(0, msg)
            curr_id = msg.parent_id
        
        for msg in branch:
            new_manager.save_message(msg)
        return new_manager

    def list_sessions(self) -> List[Dict[str, Any]]:
        sessions = []
        for f in self.sessions_dir.glob("*.jsonl"):
            sessions.append({
                "id": f.stem,
                "path": str(f),
                "modified": f.stat().st_mtime
            })
        return sorted(sessions, key=lambda x: x["modified"], reverse=True)

    def list_project_sessions(self) -> List[Dict[str, Any]]:
        sessions = self.list_sessions()
        # Filter by project (cwd in header)
        project_sessions = []
        for s in sessions:
            try:
                with open(s["path"], "r") as f:
                    header = json.loads(f.readline())
                    if header.get("cwd") == self.cwd:
                        project_sessions.append(s)
            except:
                pass
        return project_sessions

    def export_html(self) -> str:
        messages = self.get_active_branch()
        # Simple HTML dump for now
        html = "<html><body>"
        for m in messages:
            html += f"<h3>{m.role}</h3><p>{m.content}</p>"
        html += "</body></html>"
        
        out_path = self.sessions_dir / f"{self.session_id}.html"
        with open(out_path, "w") as f: f.write(html)
        return str(out_path)

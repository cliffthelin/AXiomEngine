#!/usr/bin/env python3
import json
import uuid
import time
from pathlib import Path
from typing import List, Dict, Optional, Any

class SessionEntry:
    def __init__(self, role: str, content: str, parent_id: Optional[str] = None, entry_id: Optional[str] = None):
        self.id = entry_id or str(uuid.uuid4())
        self.parent_id = parent_id
        self.role = role
        self.content = content
        self.timestamp = time.time()
        self.metadata = {}

    def to_dict(self):
        return {
            "id": self.id,
            "parentId": self.parent_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, d: dict):
        entry = cls(d["role"], d["content"], d.get("parentId"), d["id"])
        entry.timestamp = d.get("timestamp", time.time())
        entry.metadata = d.get("metadata", {})
        return entry

class SessionTree:
    """
    Implements PI Session Tree (JSONL format).
    Supports branching, forking, and tree navigation.
    """
    def __init__(self, session_file: Path):
        self.session_file = Path(session_file)
        self.entries: List[SessionEntry] = []
        self.current_branch_head: Optional[str] = None
        self._load()

    def _load(self):
        if not self.session_file.exists():
            return
        with open(self.session_file, "r") as f:
            for line in f:
                if line.strip():
                    self.entries.append(SessionEntry.from_dict(json.loads(line)))
        if self.entries:
            self.current_branch_head = self.entries[-1].id

    def save_entry(self, role: str, content: str, metadata: dict = None):
        entry = SessionEntry(role, content, self.current_branch_head)
        if metadata:
            entry.metadata = metadata
        
        self.entries.append(entry)
        self.current_branch_head = entry.id
        
        with open(self.session_file, "a") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")
        return entry

    def get_active_branch(self) -> List[SessionEntry]:
        """Returns the list of entries in the current active path."""
        if not self.current_branch_head:
            return []
        
        # Build ID lookup
        lookup = {e.id: e for e in self.entries}
        branch = []
        curr_id = self.current_branch_head
        
        while curr_id:
            entry = lookup.get(curr_id)
            if not entry: break
            branch.append(entry)
            curr_id = entry.parent_id
            
        return list(reversed(branch))

    def fork(self, entry_id: str):
        """Sets the head to a specific entry ID to start a new branch."""
        # Verify ID exists
        if any(e.id == entry_id for e in self.entries):
            self.current_branch_head = entry_id
            return True
        return False

    def get_tree_summary(self):
        """Returns a list of branches for the /tree view."""
        # In a real implementation, this would build a graph
        return self.entries

if __name__ == "__main__":
    test_path = Path("test_session.jsonl")
    tree = SessionTree(test_path)
    tree.save_entry("user", "Hello!")
    tree.save_entry("assistant", "Hi there!")
    
    branch = tree.get_active_branch()
    print(f"Branch Length: {len(branch)}")
    for e in branch:
        print(f"[{e.role}] {e.content}")
    
    # Cleanup
    if test_path.exists(): test_path.unlink()

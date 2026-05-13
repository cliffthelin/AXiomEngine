#!/usr/bin/env python3
import json
from pathlib import Path

GRAPH_FILE = Path(__file__).parent.parent / "knowledge_graph.json"

from ast_indexer import ASTIndexer

class KnowledgeGraph:
    """
    Semantic Knowledge Graph for AXiomEngine.
    Maintains relationships between entities (Files, Tasks, Concepts).
    """
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.graph = self._load()

    def _load(self):
        if GRAPH_FILE.exists():
            with open(GRAPH_FILE, "r") as f:
                return json.load(f)
        return {"nodes": [], "edges": []}

    def _save(self):
        with open(GRAPH_FILE, "w") as f:
            json.dump(self.graph, f, indent=2)

    def populate_from_ast(self):
        """Builds nodes and edges from AST structural index."""
        indexer = ASTIndexer(self.repo_path)
        index = indexer.build_index()
        
        for file_path, info in index.items():
            self.add_node(file_path, "File", {})
            for cls in info['classes']:
                cls_id = f"{file_path}::{cls['name']}"
                self.add_node(cls_id, "Class", {"line": cls['line']})
                self.add_edge(file_path, cls_id, "contains")
                for method in cls['methods']:
                    m_id = f"{cls_id}.{method}"
                    self.add_node(m_id, "Method", {})
                    self.add_edge(cls_id, m_id, "defines")
        
        print(f"KnowledgeGraph: Populated {len(self.graph['nodes'])} nodes from AST.")

    def add_node(self, node_id: str, type: str, data: dict):
        if not any(n['id'] == node_id for n in self.graph['nodes']):
            self.graph['nodes'].append({"id": node_id, "type": type, "data": data})
            self._save()

    def add_edge(self, source: str, target: str, relationship: str):
        edge = {"source": source, "target": target, "relation": relationship}
        if edge not in self.graph['edges']:
            self.graph['edges'].append(edge)
            self._save()

if __name__ == "__main__":
    kg = KnowledgeGraph(repo_path="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine")
    kg.populate_from_ast()

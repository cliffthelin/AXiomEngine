#!/usr/bin/env python3
import ast
import os
from pathlib import Path

class ASTIndexer:
    """
    Code Structure Indexer for AXiomEngine.
    Parses Python files to extract structural maps (classes, methods, functions).
    """
    def __init__(self, repo_path="."):
        self.repo_path = Path(repo_path)
        self.index = {}

    def index_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({"name": node.name, "methods": methods, "line": node.lineno})
                elif isinstance(node, ast.FunctionDef) and not getattr(node, '_is_method', False):
                    # Rough check to separate top-level functions from methods
                    functions.append({"name": node.name, "line": node.lineno})
                    
            self.index[str(file_path.relative_to(self.repo_path))] = {
                "classes": classes,
                "functions": functions
            }
        except Exception as e:
            # Skip unparseable files
            pass

    def build_index(self):
        for py_file in self.repo_path.rglob("*.py"):
            self.index_file(py_file)
        return self.index

if __name__ == "__main__":
    indexer = ASTIndexer()
    idx = indexer.build_index()
    import json
    print(json.dumps(idx, indent=2))

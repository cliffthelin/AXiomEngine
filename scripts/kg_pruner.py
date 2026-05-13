#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

KG_PATH = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/knowledge_graph.json")

def prune_kg(max_age_days=30):
    if not KG_PATH.exists():
        print("KG Pruner: No graph found.")
        return
    
    with open(KG_PATH, "r") as f:
        graph = json.load(f)
    
    initial_nodes = len(graph.get("nodes", []))
    now = time.time()
    
    # Simple pruning based on an assumed 'last_accessed' or 'created_at' field in metadata
    # If not present, we keep it.
    new_nodes = []
    for node in graph.get("nodes", []):
        ts = node.get("metadata", {}).get("timestamp", now)
        if (now - ts) < (max_age_days * 86400):
            new_nodes.append(node)
            
    graph["nodes"] = new_nodes
    # Re-filter edges
    node_ids = {n["id"] for n in new_nodes}
    graph["edges"] = [e for e in graph.get("edges", []) if e["source"] in node_ids and e["target"] in node_ids]
    
    with open(KG_PATH, "w") as f:
        json.dump(graph, f, indent=2)
    
    print(f"KG Pruner: Pruned {initial_nodes - len(new_nodes)} stale nodes.")

if __name__ == "__main__":
    prune_kg()

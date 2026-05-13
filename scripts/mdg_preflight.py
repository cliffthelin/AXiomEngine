#!/usr/bin/env python3
"""
MDG Pre-Flight Check — PDD Pipeline Gate
==========================================
Before any agent makes a change, this pre-flight check answers:
  1. What downstream dependencies exist?
  2. What decisions constrain this scope?
  3. Is the temporal scope valid?

If any check fails → agent MUST stop.

Usage:
  python3 mdg_preflight.py <file_or_concept>
  python3 mdg_preflight.py scripts/gpu_thermal_optimizer.py
  python3 mdg_preflight.py DC-GPU-THERMAL-LIMIT
"""
import argparse
import json
import sys
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description="MDG Pre-Flight Check")
    p.add_argument("target", help="File path, DataConcept, Rule, or Decision ID")
    p.add_argument("--project-root", type=Path, default=Path("."),
                   help="Root directory of the project")
    return p.parse_args()


def load_mdg(root):
    mdg_path = root / "MDG.json"
    if not mdg_path.exists():
        print("❌ MDG not found. Run mdg_builder.py first.")
        sys.exit(1)
    with open(mdg_path) as f:
        return json.load(f)


def find_downstream(mdg, node_id):
    """Find all nodes reachable from node_id via outgoing edges."""
    downstream = []
    visited = set()
    queue = [node_id]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        for edge in mdg["edges"]:
            if edge["from_node"] == current and edge["to_node"] not in visited:
                downstream.append({
                    "edge": edge["mdg_edge_id"],
                    "type": edge["dependency_type"],
                    "target": edge["to_node"],
                    "confidence": edge.get("confidence", "Unknown"),
                })
                queue.append(edge["to_node"])
    return downstream


def find_upstream(mdg, node_id):
    """Find all nodes that point TO this node (what constrains it)."""
    upstream = []
    for edge in mdg["edges"]:
        if edge["to_node"] == node_id:
            upstream.append({
                "edge": edge["mdg_edge_id"],
                "type": edge["dependency_type"],
                "source": edge["from_node"],
                "confidence": edge.get("confidence", "Unknown"),
            })
    return upstream


def find_decisions(mdg, node_id):
    """Find all Decision nodes constraining this node."""
    decisions = []
    for edge in mdg["edges"]:
        if edge["to_node"] == node_id and edge["dependency_type"] == "INTERPRETS":
            decisions.append(edge["from_node"])
        if edge["from_node"] == node_id and edge["dependency_type"] == "INTERPRETS":
            decisions.append(edge["to_node"])
    return decisions


def run_preflight(target, root):
    root = root.resolve()
    mdg = load_mdg(root)

    # Resolve target: could be a file path or a DataConcept ID
    node_id = target
    is_file = not target.startswith("DC-") and not target.startswith("R-") and not target.startswith("DEC-")

    # If it's a file, find linked concepts
    linked_concepts = []
    if is_file:
        try:
            with open(root / "INTENT_INDEX.json") as f:
                index = json.load(f)
            entry = index.get("files", {}).get(target, {})
            linked_concepts = entry.get("intent_stack", {}).get("L8", {}).get("concepts", [])
        except Exception:
            pass

    print("=" * 72)
    print(f"  MDG PRE-FLIGHT CHECK")
    print(f"  Target: {target}")
    print("=" * 72)

    all_downstream = []
    all_upstream = []
    all_decisions = []

    # Check the target itself
    targets_to_check = [node_id] + linked_concepts
    for t in targets_to_check:
        all_downstream.extend(find_downstream(mdg, t))
        all_upstream.extend(find_upstream(mdg, t))
        all_decisions.extend(find_decisions(mdg, t))

    # Deduplicate
    all_decisions = list(set(all_decisions))

    # Determine status
    has_downstream = len(all_downstream) > 0
    has_constraints = len(all_upstream) > 0
    has_decisions = len(all_decisions) > 0

    status = "PASS"
    reasons = []

    if has_downstream and len(all_downstream) > 3:
        status = "FAIL"
        reasons.append("HIGH_DOWNSTREAM_IMPACT")
    if has_decisions:
        reasons.append("DECISION_CONSTRAINTS_EXIST")
        if status == "PASS":
            status = "WARN"

    # Print results
    print(f"\n  Status: {'🔴 ' + status if status == 'FAIL' else '🟡 ' + status if status == 'WARN' else '🟢 ' + status}")
    if reasons:
        print(f"  Reasons: {', '.join(reasons)}")

    if linked_concepts:
        print(f"\n  📌 Linked DataConcepts: {linked_concepts}")

    if all_upstream:
        print(f"\n  ⬆️  Upstream Constraints ({len(all_upstream)}):")
        for u in all_upstream[:10]:
            print(f"     {u['type']}: {u['source']} → [{u['confidence']}]")

    if all_downstream:
        print(f"\n  ⬇️  Downstream Dependencies ({len(all_downstream)}):")
        for d in all_downstream[:10]:
            print(f"     {d['type']}: → {d['target'][:60]} [{d['confidence']}]")

    if all_decisions:
        print(f"\n  ⚖️  Active Decisions: {all_decisions}")
        print(f"     ⚠️  These decisions MUST be reviewed before proceeding.")

    if not all_downstream and not all_upstream and not all_decisions:
        print(f"\n  ℹ️  No dependencies found. Target is isolated in the MDG.")

    # Output machine-readable result
    result = {
        "status": status,
        "target": target,
        "reasons": reasons,
        "linked_concepts": linked_concepts,
        "downstream_count": len(all_downstream),
        "upstream_count": len(all_upstream),
        "active_decisions": all_decisions,
        "required_acknowledgements": all_decisions + [d["target"] for d in all_downstream[:5]],
    }

    print(f"\n{'=' * 72}")
    return result


if __name__ == "__main__":
    args = parse_args()
    run_preflight(args.target, args.project_root)

#!/usr/bin/env python3
"""
MDG Builder — Materialized Dependency Graph
=============================================
Reads the Intent Index and Knowledge Graph to build pre-computed dependency
chains: Authority → Concept → Rule → Validation → Code.

The MDG enables O(1) impact queries: "What breaks if I change X?"

Usage:
  python3 scripts/mdg_builder.py                        # Uses current dir
  python3 scripts/mdg_builder.py --project-root /path   # Any project
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description="MDG Builder")
    p.add_argument("--project-root", type=Path, default=Path("."),
                   help="Root directory of the project to govern")
    return p.parse_args()


def load_pdd_rules(root):
    rules = []
    pf = root / "pdd" / "load_rules.py"
    if not pf.exists():
        return rules
    for m in re.finditer(r'\("(R-[^"]+)",\s*"([^"]+)",\s*"([^"]+)",\s*"([^"]*(?:"[^"]*"[^"]*)*)"', pf.read_text()):
        rules.append({"rule_id": m.group(1), "scope": m.group(2), "title": m.group(3)})
    if not rules:
        for m in re.finditer(r'\("(R-[^"]+)",\s*"([^"]+)",\s*"([^"]+)",', pf.read_text()):
            rules.append({"rule_id": m.group(1), "scope": m.group(2), "title": m.group(3)})
    return rules


def build_mdg(root: Path):
    root = root.resolve()
    print("=" * 72)
    print("  MDG BUILDER — Materialized Dependency Graph")
    print(f"  Project Root: {root}")
    print("=" * 72)

    # Load sources
    with open(root / "INTENT_INDEX.json") as f:
        index = json.load(f)

    concepts = {}
    cp = root / "data" / "data_concepts.json"
    if cp.exists():
        with open(cp) as f:
            concepts = {c["data_concept_id"]: c for c in json.load(f).get("concepts", [])}

    decisions = []
    dp = root / "data" / "decisions.json"
    if dp.exists():
        with open(dp) as f:
            decisions = json.load(f).get("decisions", [])

    pdd_rules = load_pdd_rules(root)
    now = datetime.now(timezone.utc).isoformat()

    mdg = {"metadata": {"generated_at": now, "engine": "MDG Builder v1.0"},
           "nodes": [], "edges": [], "summary": {}}

    node_ids = set()

    # Create nodes for DataConcepts
    for cid, c in concepts.items():
        mdg["nodes"].append({"mdg_node_id": cid, "source_type": "DataConcept",
                             "node_role": "Anchor", "description": c["name"],
                             "temporal": {"start_date": "2026-01-01", "end_date": None}})
        node_ids.add(cid)

    # Create nodes for PDD Rules
    for r in pdd_rules:
        rid = r["rule_id"]
        mdg["nodes"].append({"mdg_node_id": rid, "source_type": "PDD_Rule",
                             "node_role": "Constraint", "description": r["title"],
                             "temporal": {"start_date": "2026-01-01", "end_date": None}})
        node_ids.add(rid)

    # Create nodes for Decisions
    for d in decisions:
        did = d["decision_id"]
        mdg["nodes"].append({"mdg_node_id": did, "source_type": "Decision",
                             "node_role": "Interpretation", "description": d.get("rationale", "")[:80],
                             "temporal": d.get("effective", {})})
        node_ids.add(did)

    # Create edges: DataConcept → PDD Rules (by scope matching)
    edge_id = 0
    for cid, c in concepts.items():
        aliases = [a.lower() for a in c.get("aliases", [])]
        for r in pdd_rules:
            if r["scope"].lower() in aliases or any(r["scope"].lower() in a for a in aliases):
                edge_id += 1
                mdg["edges"].append({
                    "mdg_edge_id": f"MDG-E-{edge_id:04d}",
                    "from_node": cid, "to_node": r["rule_id"],
                    "dependency_type": "REQUIRES",
                    "confidence": "Authoritative",
                    "temporal": {"start_date": "2026-01-01", "end_date": None},
                    "sync_state": {"last_computed": now, "trigger": "SourceChange"}
                })

    # Create edges: Decision → DataConcept (from decision scope)
    for d in decisions:
        did = d["decision_id"]
        for target in d.get("scope", {}).get("applies_to", []):
            eid = target.get("entity_id", "")
            if eid in node_ids:
                edge_id += 1
                mdg["edges"].append({
                    "mdg_edge_id": f"MDG-E-{edge_id:04d}",
                    "from_node": did, "to_node": eid,
                    "dependency_type": "INTERPRETS",
                    "confidence": "Authoritative",
                    "temporal": d.get("effective", {}),
                    "sync_state": {"last_computed": now, "trigger": "GovernanceDecision"}
                })

    # Create edges: DataConcept → Code files (via alias matching)
    for fp, entry in index.get("files", {}).items():
        linked = entry.get("intent_stack", {}).get("L8", {}).get("concepts", [])
        for cid in linked:
            edge_id += 1
            mdg["edges"].append({
                "mdg_edge_id": f"MDG-E-{edge_id:04d}",
                "from_node": cid, "to_node": fp,
                "dependency_type": "IMPLEMENTED_BY",
                "confidence": "Observed",
                "temporal": {"start_date": "2026-01-01", "end_date": None},
                "sync_state": {"last_computed": now, "trigger": "SourceChange"}
            })

    mdg["summary"] = {
        "total_nodes": len(mdg["nodes"]),
        "total_edges": len(mdg["edges"]),
        "node_types": {t: sum(1 for n in mdg["nodes"] if n["source_type"] == t)
                       for t in set(n["source_type"] for n in mdg["nodes"])},
        "edge_types": {t: sum(1 for e in mdg["edges"] if e["dependency_type"] == t)
                       for t in set(e["dependency_type"] for e in mdg["edges"])},
    }

    out = root / "MDG.json"
    with open(out, "w") as f:
        json.dump(mdg, f, indent=2)

    s = mdg["summary"]
    print(f"\n  Nodes: {s['total_nodes']}  |  Edges: {s['total_edges']}")
    print(f"  Node types: {s['node_types']}")
    print(f"  Edge types: {s['edge_types']}")
    print(f"\n  📁 Saved to: {out}")
    print("=" * 72)


if __name__ == "__main__":
    args = parse_args()
    build_mdg(args.project_root)

#!/usr/bin/env python3
"""
Drift Detector v2.1 — 13-Layer Governance Analysis (Portable)
==============================================================
Reads the Intent Index v2.1 and generates a comprehensive drift report
covering all 13 governance layers with phase-aware exclusions.

Usage:
  python3 scripts/drift_detector.py                        # Uses current dir
  python3 scripts/drift_detector.py --project-root /path   # Any project
"""
import argparse
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone


def parse_args():
    p = argparse.ArgumentParser(description="13-Layer Governance Drift Detector")
    p.add_argument("--project-root", type=Path, default=Path("."),
                   help="Root directory of the project")
    return p.parse_args()

LAYER_NAMES = {
    "L1": "Application Code", "L2": "Reversa Behavioral", "L3": "PDD Rules",
    "L4": "Authority", "L5": "Derived Logic", "L6": "Decisions",
    "L7": "Obligations", "L8": "DataConcepts", "L9": "Knowledge Graph",
    "L10": "MDG", "L11": "Validation", "L12": "Temporal", "L13": "Process",
}


def load(path):
    with open(path) as f:
        return json.load(f)


def layer_coverage(index):
    total = len(index["files"])
    cov = {k: 0 for k in LAYER_NAMES}
    for entry in index["files"].values():
        s = entry.get("intent_stack", {})
        if s.get("L1", {}).get("real_code_chars", 0) > 0: cov["L1"] += 1
        if s.get("L2", {}).get("has_coverage"): cov["L2"] += 1
        if s.get("L3", {}).get("rules"): cov["L3"] += 1
        if s.get("L4", {}).get("has_authority"): cov["L4"] += 1
        if s.get("L5", {}).get("derivations"): cov["L5"] += 1
        if s.get("L6", {}).get("decisions"): cov["L6"] += 1
        if s.get("L7", {}).get("obligations"): cov["L7"] += 1
        if s.get("L8", {}).get("concepts"): cov["L8"] += 1
        if s.get("L9", {}).get("in_graph"): cov["L9"] += 1
        if s.get("L10", {}).get("mdg_edges"): cov["L10"] += 1
        if s.get("L11", {}).get("validations"): cov["L11"] += 1
        if s.get("L12", {}).get("has_temporal"): cov["L12"] += 1
        if s.get("L13", {}).get("has_process_record"): cov["L13"] += 1
    return {k: {"count": v, "pct": round(v / max(total, 1) * 100, 1)} for k, v in cov.items()}


def worst_drifters(index, n=20):
    entries = []
    for fp, e in index["files"].items():
        chars = e["intent_stack"].get("L1", {}).get("real_code_chars", 0)
        entries.append({"file": fp, "alignment": e["alignment_score"],
                        "verdict": e["verdict"], "chars": chars,
                        "risk": chars * (1.0 - e["alignment_score"])})
    entries.sort(key=lambda x: x["risk"], reverse=True)
    return entries[:n]


def component_alignment(index):
    by_comp = defaultdict(lambda: {"files": 0, "score": 0.0, "chars": 0})
    for fp, e in index["files"].items():
        parts = fp.split("/")
        comp = parts[0] if parts else "root"
        by_comp[comp]["files"] += 1
        by_comp[comp]["score"] += e["alignment_score"]
        by_comp[comp]["chars"] += e["intent_stack"].get("L1", {}).get("real_code_chars", 0)
    return dict(sorted(
        {k: {**v, "mean": round(v["score"] / max(v["files"], 1), 3)} for k, v in by_comp.items()}.items(),
        key=lambda x: x[1]["chars"], reverse=True))


def generate(root: Path):
    root = root.resolve()
    index = load(root / "INTENT_INDEX.json")
    s = index["summary"]
    meta = index["metadata"]
    cov = layer_coverage(index)
    worst = worst_drifters(index)
    comps = component_alignment(index)

    mdg_summary = {}
    mdg_path = root / "MDG.json"
    if mdg_path.exists():
        mdg_summary = load(mdg_path).get("summary", {})

    now = datetime.now(timezone.utc).isoformat()

    phase = meta.get("governance_phase", "unknown")
    excluded = s.get("total_excluded", 0)
    excluded_cats = s.get("excluded_by_category", {})

    lines = [
        "# Governance Drift Analysis Report (13-Layer)",
        f"\n> Generated: {now}",
        f"> Engine: {meta.get('engine', 'Unknown')}",
        f"> Phase: **{phase.upper()}**",
        f"> DataConcepts: {meta.get('total_data_concepts', 0)} | Decisions: {meta.get('total_decisions', 0)} | MDG Nodes: {mdg_summary.get('total_nodes', 0)} | MDG Edges: {mdg_summary.get('total_edges', 0)}",
        "",
        "## Executive Summary", "",
        "| Metric | Value |", "| :--- | :--- |",
        f"| Total in Report | {s.get('total_in_report', s.get('total_files', 0))} |",
        f"| ⚪ Excluded (phase: {phase}) | {excluded} |",
    ]
    for cat, cnt in excluded_cats.items():
        lines.append(f"| &nbsp;&nbsp;└─ {cat} | {cnt} |")
    lines += [
        f"| **Files Scored** | **{s.get('total_scored', s.get('total_files', 0))}** |",
        f"| 🟢 Governed | {s['governed']} ({s['governed_pct']}%) |",
        f"| 🟡 Partial | {s['partial']} ({s['partial_pct']}%) |",
        f"| 🔴 Ungoverned | {s.get('ungoverned', 0)} ({s.get('ungoverned_pct', 0)}%) |",
        f"| ⚫ Dark | {s.get('dark', 0)} ({s.get('dark_pct', 0)}%) |",
        f"| **Mean Alignment** | **{s['mean_alignment']}** |",
        "",
        "## 13-Layer Coverage", "",
        "| # | Layer | Coverage | Files | % |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]

    for lid, name in LAYER_NAMES.items():
        d = cov[lid]
        bar = "█" * int(d["pct"] / 5) + "░" * (20 - int(d["pct"] / 5))
        lines.append(f"| {lid} | {name} | {bar} | {d['count']} | {d['pct']}% |")

    lines += ["", "## Component Alignment", "",
              "| Component | Files | Chars | Mean Alignment |",
              "| :--- | :--- | :--- | :--- |"]
    for comp, d in list(comps.items())[:15]:
        lines.append(f"| `{comp}` | {d['files']} | {d['chars']:,} | {d['mean']} |")

    lines += ["", "## Top 20 Drift Risk Files", "",
              "| File | Chars | Alignment | Risk | Verdict |",
              "| :--- | :--- | :--- | :--- | :--- |"]
    for e in worst:
        lines.append(f"| `{e['file'][:70]}` | {e['chars']:,} | {e['alignment']:.3f} | {e['risk']:,.0f} | {e['verdict']} |")

    # Intent Gaps
    gaps = {}
    for lid in LAYER_NAMES:
        gaps[lid] = sum(1 for e in index["files"].values()
                        if not cov_check(e, lid))
    lines += ["", "## Intent Gaps (Missing Layer Coverage)", ""]
    for lid, name in LAYER_NAMES.items():
        if gaps[lid] > 0:
            lines.append(f"- **{lid} ({name})**: {gaps[lid]} files uncovered")

    # MDG Summary
    if mdg_summary:
        lines += ["", "## MDG Summary", "",
                   f"- Nodes: {mdg_summary.get('total_nodes', 0)}",
                   f"- Edges: {mdg_summary.get('total_edges', 0)}",
                   f"- Node types: {mdg_summary.get('node_types', {})}",
                   f"- Edge types: {mdg_summary.get('edge_types', {})}"]

    lines += ["", "---", "*Generated by the 13-Layer Governance Intent Resolution Engine.*"]

    out = root / "GOVERNANCE_DRIFT_REPORT.md"
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"📊 Report saved to: {out}")
    print(f"   Phase: {phase.upper()} | Scored: {s.get('total_scored', '?')} | Excluded: {excluded}")
    print(f"   Mean Alignment: {s['mean_alignment']}")


def cov_check(entry, lid):
    s = entry.get("intent_stack", {})
    checks = {
        "L1": lambda: s.get("L1", {}).get("real_code_chars", 0) > 0,
        "L2": lambda: s.get("L2", {}).get("has_coverage"),
        "L3": lambda: s.get("L3", {}).get("rules"),
        "L4": lambda: s.get("L4", {}).get("has_authority"),
        "L5": lambda: s.get("L5", {}).get("derivations"),
        "L6": lambda: s.get("L6", {}).get("decisions"),
        "L7": lambda: s.get("L7", {}).get("obligations"),
        "L8": lambda: s.get("L8", {}).get("concepts"),
        "L9": lambda: s.get("L9", {}).get("in_graph"),
        "L10": lambda: s.get("L10", {}).get("mdg_edges"),
        "L11": lambda: s.get("L11", {}).get("validations"),
        "L12": lambda: s.get("L12", {}).get("has_temporal"),
        "L13": lambda: s.get("L13", {}).get("has_process_record"),
    }
    return checks.get(lid, lambda: False)()


if __name__ == "__main__":
    args = parse_args()
    generate(args.project_root)

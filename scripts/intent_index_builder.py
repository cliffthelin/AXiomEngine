#!/usr/bin/env python3
"""
Intent Index Builder v2.1 — 13-Layer Governance Resolution Engine
==================================================================
Portable, phase-aware governance indexer.

Usage:
  python3 scripts/intent_index_builder.py                        # Uses current dir
  python3 scripts/intent_index_builder.py --project-root /path   # Any project
"""
import argparse
import fnmatch
import json
import re
from datetime import datetime, timezone
from pathlib import Path

LANG_MAP = {
    ".py": "python", ".ts": "typescript", ".js": "javascript",
    ".md": "markdown", ".json": "json", ".sh": "bash",
    ".toml": "toml", ".yml": "yaml", ".yaml": "yaml",
    ".css": "css", ".html": "html", ".tsx": "tsx",
}

LAYER_WEIGHTS = {
    "L1_code": 0.08, "L2_reversa": 0.12, "L3_pdd_rules": 0.10,
    "L4_authority": 0.10, "L5_derived": 0.05, "L6_decisions": 0.10,
    "L7_obligations": 0.05, "L8_data_concepts": 0.15,
    "L9_knowledge_graph": 0.05, "L10_mdg": 0.05,
    "L11_validation": 0.05, "L12_temporal": 0.05, "L13_process": 0.05,
}


def parse_args():
    p = argparse.ArgumentParser(description="13-Layer Governance Intent Index Builder")
    p.add_argument("--project-root", type=Path, default=Path("."),
                   help="Root directory of the project to govern")
    return p.parse_args()


# ── Phase-Aware Filtering ──────────────────────────────────────

def load_governance_config(root: Path) -> dict:
    cfg_path = root / "data" / "governance_config.json"
    if not cfg_path.exists():
        return {"governance_phase": "discovery", "phase_rules": {
            "discovery": {"include_tests": True, "include_generated": True,
                          "include_changelogs": False, "include_lockfiles": False}
        }, "exclusion_patterns": {}}
    with open(cfg_path) as f:
        return json.load(f)


def should_exclude(filepath: str, config: dict) -> str | None:
    """Returns exclusion reason or None if file should be scored."""
    phase = config.get("governance_phase", "discovery")
    rules = config.get("phase_rules", {}).get(phase, {})
    patterns = config.get("exclusion_patterns", {})

    checks = [
        ("tests", "include_tests"),
        ("generated", "include_generated"),
        ("changelogs", "include_changelogs"),
        ("lockfiles", "include_lockfiles"),
    ]

    for category, rule_key in checks:
        if not rules.get(rule_key, True):
            for pattern in patterns.get(category, []):
                if fnmatch.fnmatch(Path(filepath).name, pattern):
                    return category
                # Also check path-based patterns
                if "/" in pattern and fnmatch.fnmatch(filepath, pattern):
                    return category
    return None


# ── Layer Loaders ──────────────────────────────────────────────

def load_knowledge_graph(root: Path):
    p = root / "knowledge_graph.json"
    if not p.exists():
        return {}
    with open(p) as f:
        kg = json.load(f)
    nodes = {}
    for n in kg.get("nodes", []):
        base = n["id"].split("::")[0]
        if base not in nodes:
            nodes[base] = {"symbols": [], "type": n.get("type", "Unknown")}
        if "::" in n["id"]:
            nodes[base]["symbols"].append(n["id"].split("::")[-1])
    return nodes


def load_pdd_rules(root: Path):
    p = root / "pdd" / "load_rules.py"
    if not p.exists():
        return []
    rules = []
    for m in re.finditer(r'\("(R-[^"]+)",\s*"([^"]+)",\s*"([^"]+)",', p.read_text()):
        rules.append({"rule_id": m.group(1), "scope": m.group(2), "title": m.group(3)})
    return rules


def load_global_queue(root: Path):
    p = root / "docs" / "GLOBAL_IMPLEMENTATION_QUEUE.md"
    if not p.exists():
        return {}
    result = {}
    with open(p) as f:
        for line in f:
            m = re.match(r'\|\s*(G-[^\s|]+)\s*\|\s*([^\s|]+)\s*\|', line)
            if m:
                result.setdefault(m.group(2).strip(), []).append(m.group(1).strip())
    return result


def load_governance_report(root: Path):
    p = root / "AXIOMENGINE_GOVERNANCE_REPORT.md"
    if not p.exists():
        return {}
    metrics = {}
    with open(p) as f:
        for line in f:
            m = re.match(
                r'\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([^\s|]+)\s*\|\s*([^|]+)\|',
                line)
            if m:
                metrics[m.group(1)] = {
                    "lines": int(m.group(2)), "rules_mapped": int(m.group(3)),
                    "real_code_chars": int(m.group(4)), "real_context_chars": int(m.group(5)),
                    "ratio": m.group(6).strip(), "status": m.group(7).strip(),
                }
    return metrics


def load_reversa_sdd(root: Path):
    p = root / "_reversa_sdd"
    if not p.exists():
        return {}
    artifacts = {}
    for md in p.rglob("*.md"):
        rel = str(md.relative_to(root))
        content = md.read_text(errors="ignore")
        rules = [l.strip()[:200] for l in content.split("\n")
                 if any(k in l for k in ["🟢", "🟡", "🔴", "CONFIRMED", "INFERRED", "Gap"])]
        artifacts[rel] = {"path": rel, "size": md.stat().st_size, "rules_found": len(rules)}
    return artifacts


def load_data_concepts(root: Path):
    p = root / "data" / "data_concepts.json"
    if not p.exists():
        return {}
    with open(p) as f:
        return {c["data_concept_id"]: c for c in json.load(f).get("concepts", [])}


def load_decisions(root: Path):
    p = root / "data" / "decisions.json"
    if not p.exists():
        return []
    with open(p) as f:
        return json.load(f).get("decisions", [])


def count_process_records(root: Path):
    p = root / "data" / "process_records"
    if not p.exists():
        return 0
    return sum(1 for _ in p.glob("*.yaml")) + sum(1 for _ in p.glob("*.yml"))


# ── Scoring ────────────────────────────────────────────────────

def compute_alignment(stack):
    score = 0.0
    if stack.get("L1", {}).get("real_code_chars", 0) > 0: score += LAYER_WEIGHTS["L1_code"]
    if stack.get("L2", {}).get("has_coverage"): score += LAYER_WEIGHTS["L2_reversa"]
    if stack.get("L3", {}).get("rules"): score += LAYER_WEIGHTS["L3_pdd_rules"]
    if stack.get("L4", {}).get("has_authority"): score += LAYER_WEIGHTS["L4_authority"]
    if stack.get("L5", {}).get("derivations"): score += LAYER_WEIGHTS["L5_derived"]
    if stack.get("L6", {}).get("decisions"): score += LAYER_WEIGHTS["L6_decisions"]
    if stack.get("L7", {}).get("obligations"): score += LAYER_WEIGHTS["L7_obligations"]
    if stack.get("L8", {}).get("concepts"): score += LAYER_WEIGHTS["L8_data_concepts"]
    if stack.get("L9", {}).get("in_graph"): score += LAYER_WEIGHTS["L9_knowledge_graph"]
    if stack.get("L10", {}).get("mdg_edges"): score += LAYER_WEIGHTS["L10_mdg"]
    if stack.get("L11", {}).get("validations"): score += LAYER_WEIGHTS["L11_validation"]
    if stack.get("L12", {}).get("has_temporal"): score += LAYER_WEIGHTS["L12_temporal"]
    if stack.get("L13", {}).get("has_process_record"): score += LAYER_WEIGHTS["L13_process"]
    return round(score, 3)


def classify(score):
    if score >= 0.75: return "🟢 GOVERNED"
    if score >= 0.40: return "🟡 PARTIAL"
    if score > 0.08: return "🔴 UNGOVERNED"
    return "⚫ DARK"


# ── Main ───────────────────────────────────────────────────────

def build(root: Path):
    root = root.resolve()
    print("=" * 72)
    print("  INTENT INDEX v2.1 — 13-Layer Governance Resolution Engine")
    print(f"  Project Root: {root}")
    print("=" * 72)

    # Load config
    config = load_governance_config(root)
    phase = config.get("governance_phase", "discovery")
    print(f"\n  📋 Governance Phase: {phase.upper()}")

    # Load layers
    print("\n📊 Loading governance layers...")
    kg = load_knowledge_graph(root)
    print(f"  [L9  Knowledge Graph]  {len(kg)} nodes")
    pdd = load_pdd_rules(root)
    print(f"  [L3  PDD Rules]        {len(pdd)} rules")
    queue = load_global_queue(root)
    q_total = sum(len(v) for v in queue.values())
    print(f"  [L3b Global Queue]     {q_total} mappings across {len(queue)} sources")
    report = load_governance_report(root)
    print(f"  [L1  Code Reality]     {len(report)} files")
    sdd = load_reversa_sdd(root)
    print(f"  [L2  Reversa SDD]      {len(sdd)} artifacts")
    concepts = load_data_concepts(root)
    print(f"  [L8  DataConcepts]     {len(concepts)} concepts")
    decisions = load_decisions(root)
    print(f"  [L6  Decisions]        {len(decisions)} decisions")
    proc_count = count_process_records(root)
    print(f"  [L13 ProcessRecords]   {proc_count} records")

    schema_exists = (root / "data" / "governance_schema.yaml").exists()
    print(f"  [Schema]               {'✅' if schema_exists else '❌'}")

    # Build index
    index = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "engine": "Intent Index v2.1 — 13-Layer (Portable, Phase-Aware)",
            "project_root": str(root),
            "governance_phase": phase,
            "layer_count": 13,
            "total_pdd_rules": len(pdd), "total_queue_rules": q_total,
            "total_sdd_artifacts": len(sdd), "total_data_concepts": len(concepts),
            "total_decisions": len(decisions), "total_kg_nodes": len(kg),
            "total_process_records": proc_count, "schema_present": schema_exists,
        },
        "files": {}, "excluded_files": {}, "data_concepts": concepts,
        "decisions": decisions, "summary": {},
    }

    verdicts = {"governed": 0, "partial": 0, "ungoverned": 0, "dark": 0}
    excluded_count = 0
    excluded_by_category = {}

    for fp, met in report.items():
        bn = Path(fp).name
        lang = LANG_MAP.get(Path(fp).suffix.lower(), "unknown")

        # Phase-aware exclusion check
        reason = should_exclude(fp, config)
        if reason:
            index["excluded_files"][fp] = {"reason": reason, "lines": met["lines"],
                                            "chars": met["real_code_chars"]}
            excluded_count += 1
            excluded_by_category[reason] = excluded_by_category.get(reason, 0) + 1
            continue

        # L2
        has_sdd = any(fp in p or bn in p for p in sdd)
        # L3
        file_rules = [r["rule_id"] for r in pdd
                       if r["scope"] in fp.lower() or (r["scope"] == "core" and lang == "python")]
        file_queue = queue.get(bn, [])
        # L4
        has_auth = any(r["scope"] in ("hw", "gov", "audit", "core")
                       for r in pdd if r["rule_id"] in file_rules)
        # L8
        linked_concepts = [cid for cid, c in concepts.items()
                          if any(a.lower() in fp.lower() for a in c.get("aliases", []))]
        # L6
        linked_decisions = [d["decision_id"] for d in decisions
                           if any(fp in str(e.get("entity_id", ""))
                                  for e in d.get("scope", {}).get("applies_to", []))]
        # L9
        in_kg = fp in kg
        symbols = kg.get(fp, {}).get("symbols", [])[:10]

        stack = {
            "L1": {"lines": met["lines"], "real_code_chars": met["real_code_chars"],
                   "real_context_chars": met["real_context_chars"],
                   "ratio": met["ratio"], "language": lang, "status": met["status"]},
            "L2": {"has_coverage": has_sdd, "confidence": "confirmed" if has_sdd else "unmapped"},
            "L3": {"rules": file_rules + file_queue, "rule_count": len(file_rules) + len(file_queue)},
            "L4": {"has_authority": has_auth},
            "L5": {"derivations": []},
            "L6": {"decisions": linked_decisions},
            "L7": {"obligations": []},
            "L8": {"concepts": linked_concepts},
            "L9": {"in_graph": in_kg, "symbols": symbols},
            "L10": {"mdg_edges": []},
            "L11": {"validations": []},
            "L12": {"has_temporal": False},
            "L13": {"has_process_record": proc_count > 0},
        }

        score = compute_alignment(stack)
        verdict = classify(score)
        index["files"][fp] = {"file": fp, "intent_stack": stack,
                              "alignment_score": score, "verdict": verdict}

        if "GOVERNED" in verdict: verdicts["governed"] += 1
        elif "PARTIAL" in verdict: verdicts["partial"] += 1
        elif "UNGOVERNED" in verdict: verdicts["ungoverned"] += 1
        else: verdicts["dark"] += 1

    scored = len(index["files"])
    index["summary"] = {
        "total_in_report": len(report),
        "total_scored": scored,
        "total_excluded": excluded_count,
        "excluded_by_category": excluded_by_category,
        **{k: v for k, v in verdicts.items()},
        **{f"{k}_pct": round(v / max(scored, 1) * 100, 1) for k, v in verdicts.items()},
        "mean_alignment": round(
            sum(e["alignment_score"] for e in index["files"].values()) / max(scored, 1), 3),
    }

    out = root / "INTENT_INDEX.json"
    with open(out, "w") as f:
        json.dump(index, f, indent=2)

    # Print summary
    s = index["summary"]
    print(f"\n{'=' * 72}")
    print(f"  INTENT INDEX v2.1 — SUMMARY (Phase: {phase.upper()})")
    print(f"{'=' * 72}")
    print(f"  Files in Report:      {s['total_in_report']}")
    print(f"  ⚪ Excluded:           {s['total_excluded']}")
    if excluded_by_category:
        for cat, cnt in excluded_by_category.items():
            print(f"     └─ {cat}: {cnt}")
    print(f"  Files Scored:         {s['total_scored']}")
    print(f"  🟢 Governed:          {s['governed']} ({s['governed_pct']}%)")
    print(f"  🟡 Partial:           {s['partial']} ({s['partial_pct']}%)")
    print(f"  🔴 Ungoverned:        {s['ungoverned']} ({s['ungoverned_pct']}%)")
    print(f"  ⚫ Dark:              {s['dark']} ({s['dark_pct']}%)")
    print(f"  Mean Alignment:       {s['mean_alignment']}")
    print(f"\n  📁 Saved to: {out}")
    print(f"{'=' * 72}")


if __name__ == "__main__":
    args = parse_args()
    build(args.project_root)

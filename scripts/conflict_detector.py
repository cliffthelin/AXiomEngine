#!/usr/bin/env python3
"""
Governance Conflict Detector
===========================
Role: Analyzes the 13-layer stack for logical contradictions.
Owner: Hermes (Determination Layer)
"""
import argparse
import json
import httpx
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", type=Path, default=Path("/mnt/UBUNTU_8TB/Projects/axiomengine"))
    return p.parse_args()

def detect_conflicts(root):
    print("🧠 Hermes is performing a Cohesiveness Audit (Conflict Detection)...")
    
    # 1. Load Core PDD Rules
    catalog_path = root / "data" / "catalog" / "PDD"
    rules = []
    if catalog_path.exists():
        for rule_file in catalog_path.glob("*.json"):
            try:
                rules.append(json.loads(rule_file.read_text()))
            except:
                pass
    
    # Also add a few samples from other domains if needed
    
    # 2. Load Decisions (L6)
    decisions_path = root / "data" / "decisions.json"
    decisions = []
    if decisions_path.exists():
        decisions = json.loads(decisions_path.read_text()).get("decisions", [])

    print(f"📊 Analyzing {len(rules)} Rules and {len(decisions)} Decisions...")

    # For now, let's cross-check every Decision against every Rule in the same 'scope'
    conflicts = []
    
    for dec in decisions:
        dec_scope = [s['entity_id'] for s in dec.get('scope', {}).get('applies_to', [])]
        
        for rule in rules:
            # Simple heuristic: if they share a DataConcept or ID, they might conflict
            # In a more advanced version, we'd use embeddings or full-matrix LLM check
            
            prompt = (
                "You are Hermes, the Governance Determination Agent. Analyze these two "
                "governance statements and determine if they CONTRADICT each other or "
                "create LOGICAL AMBIGUITY. Return a JSON object with 'conflict': true/false "
                "and 'rationale'.\n\n"
                f"STATEMENT A (Decision {dec['decision_id']}):\n{dec['statement']}\n\n"
                f"STATEMENT B (Rule):\n{json.dumps(rule)}\n"
            )

            payload = {
                "model": "qwen3.6:27b",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }

            try:
                print(f"⚖️ Comparing {dec['decision_id']} vs Rule...")
                with httpx.Client(timeout=600.0) as client:
                    resp = client.post("http://127.0.0.1:11434/v1/chat/completions", json=payload)
                    resp.raise_for_status()
                    result = json.loads(resp.json()['choices'][0]['message']['content'])
                    
                    if result.get('conflict'):
                        print(f"🚨 CONFLICT DETECTED: {dec['decision_id']}")
                        conflicts.append({
                            "a": dec['decision_id'],
                            "b": rule.get('id', 'Unknown'),
                            "rationale": result.get('rationale')
                        })
            except Exception as e:
                print(f"⚠️ Analysis error: {e}")

    # Save findings
    out = root / "data" / "governance_conflicts.json"
    with open(out, "w") as f:
        json.dump({"conflicts": conflicts, "audit_date": json.dumps(str(Path(".").absolute()))}, f, indent=2)
    
    print(f"\n✅ Cohesiveness Audit Complete. {len(conflicts)} conflicts found.")
    print(f"📁 Report: {out}")

if __name__ == "__main__":
    args = parse_args()
    detect_conflicts(args.project_root)

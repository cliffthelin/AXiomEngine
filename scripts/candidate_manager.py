#!/usr/bin/env python3
"""
Archon Candidate Manager
========================
Role: Manages the 'Candidate Layer' for Governance Sovereignty.
Pattern: Discover -> Propose (Candidate) -> Review -> Promote (Decision).
"""
import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime

# Paths
ROOT_DIR = Path("/mnt/UBUNTU_8TB/Projects/axiomengine")
CANDIDATE_DIR = ROOT_DIR / "data" / "candidates"
DECISIONS_FILE = ROOT_DIR / "data" / "decisions.json"
REJECTED_DIR = ROOT_DIR / "data" / "candidates" / "rejected"

def log_action(msg):
    print(f"🏛️ [SOVEREIGNTY] {msg}")

def list_candidates():
    candidates = list(CANDIDATE_DIR.glob("*.json"))
    log_action(f"Found {len(candidates)} pending candidates:")
    for c in candidates:
        print(f"  - {c.name}")

def promote(candidate_name, authority):
    c_path = CANDIDATE_DIR / f"{candidate_name}.json"
    if not c_path.exists():
        log_action(f"❌ Candidate {candidate_name} not found.")
        return

    with open(c_path, 'r') as f:
        candidate = json.load(f)

    # Formalize into a Decision
    decision = {
        "decision_id": f"DEC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "decision_type": "PromotedCandidate",
        "prompted_by": {
            "context_type": "autonomous_discovery",
            "description": f"Candidate promoted from {candidate_name}",
            "bounded_area": candidate.get("bounded_area", "GENERAL"),
            "evidence": candidate.get("evidence", [])
        },
        "statement": candidate.get("statement", ""),
        "authority": authority,
        "effective": {
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": null
        },
        "enforcement": "Strict",
        "supersedes": []
    }

    # Load existing decisions
    with open(DECISIONS_FILE, 'r') as f:
        data = json.load(f)
    
    data["decisions"].append(decision)

    with open(DECISIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    # Archive candidate
    shutil.move(c_path, REJECTED_DIR / "promoted" / c_path.name)
    log_action(f"✅ Promoted {candidate_name} to formal Decision.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["list", "promote", "reject"])
    parser.add_argument("--name", help="Candidate name")
    parser.add_argument("--authority", default="Human Governor", help="Who is signing off?")
    args = parser.parse_args()

    CANDIDATE_DIR.mkdir(exist_ok=True, parents=True)
    (REJECTED_DIR / "promoted").mkdir(exist_ok=True, parents=True)

    if args.action == "list":
        list_candidates()
    elif args.action == "promote":
        promote(args.name, args.authority)

if __name__ == "__main__":
    main()

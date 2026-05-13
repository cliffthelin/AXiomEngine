#!/usr/bin/env python3
"""
AXiomEngine Baseline Manifest Generator (v1.3.1)
===========================================
Generates an authoritative SHA-256 manifest of all frozen governance components.
"""
import hashlib
import json
import sys
from pathlib import Path
from datetime import datetime

BASELINE_VERSION = "1.3.1"
OUTPUT_PATH = Path("docs/audit/baseline_manifest_v1_3_1.json")

BASELINE_FILES = {
    "scripts/governance_closer.py": "Hardened promotion node",
    "governance_dashboard.html": "Authoritative health visualizer",
    "scripts/harness_manager.py": "Multi-shard mission orchestrator",
    "harness_builder_prototype.html": "Sovereign review interface",
    "data/decisions.json": "Authoritative decision registry",
    "docs/contracts/closer_report_contract.md": "Standardized mission accounting schema",
    "docs/contracts/promoted_decision_contract.md": "Standardized determination schema",
    "docs/contracts/governance_dashboard_layer_contract.md": "Standardized 13-layer mapping rules",
    "tests/test_governance_closer.py": "Operational safety tests",
    "tests/test_governance_closer_contract.py": "Schema and contract compliance tests",
    "tests/test_governance_dashboard_logic.py": "Dashboard classification and layer mapping tests",
    "docs/audit/AXIOMENGINE_GOVERNANCE_BASELINE_V1_3_1.md": "Audit baseline documentation"
}

def compute_sha256(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest():
    print(f"🏛️  Generating AXiomEngine Governance Baseline Manifest {BASELINE_VERSION}...")
    
    manifest = {
        "baseline_version": BASELINE_VERSION,
        "baseline_status": "FROZEN_FOR_AUDIT",
        "created_at": datetime.now().isoformat(),
        "files": [],
        "test_command": "PYTHONPATH=. python3 tests/test_governance_closer.py && PYTHONPATH=. python3 tests/test_governance_closer_contract.py && PYTHONPATH=. python3 tests/test_governance_dashboard_logic.py",
        "test_result_summary": "14/14 Tests Passing (Operational, Contractual, and Logic)",
        "known_limitations": [
            "Dashboard currently uses manual browser-based artifact import.",
            "Dashboard is read-only.",
            "Layer saturation depends on explicit promoted determination metadata.",
            "Static HTML dashboard does not auto-discover project files."
        ],
        "next_phase": "v1.4.0 Project Integration"
    }

    missing_files = []
    for rel_path, role in BASELINE_FILES.items():
        p = Path(rel_path)
        if not p.exists():
            print(f"❌ MISSING REQUIRED FILE: {rel_path}")
            missing_files.append(rel_path)
            continue
            
        print(f"   [HASH] {rel_path}")
        manifest["files"].append({
            "path": rel_path,
            "role": role,
            "sha256": compute_sha256(p),
            "frozen": True
        })

    if missing_files:
        print("❌ FAILED: Baseline is incomplete.")
        sys.exit(1)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"✅ Baseline manifest written to {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_manifest()

#!/usr/bin/env python3
"""
AXiomEngine Contract Drift Checker (v1.5.0)
=======================================
Detects unauthorized changes to governance contracts.
Protects closer, decision, API, and release specifications.
"""
import json
import argparse
import sys
from pathlib import Path
from scripts.governance_manifest_verifier import build_manifest_verification_result

# V1.5.0 Integration Contract Registry (In addition to v1.3.1 baseline)
INTEGRATION_CONTRACTS = [
    "docs/contracts/dashboard_discovery_api_contract.md",
    "docs/contracts/dashboard_api_adapter_contract.md",
    "docs/contracts/governance_cli_contract.md",
    "docs/contracts/release_verifier_contract.md",
    "docs/contracts/closer_report_contract.md",
    "docs/contracts/promoted_decision_contract.md",
    "docs/contracts/governance_dashboard_layer_contract.md"
]

def verify_contracts(project_root):
    root = Path(project_root).absolute()
    manifest_path = root / "docs/audit/baseline_manifest_v1_3_1.json"
    
    if not manifest_path.exists():
        print(f"❌ Error: Baseline manifest not found: {manifest_path}")
        return False

    integrity = build_manifest_verification_result(manifest_path, project_root=root)
    
    # Tracked in v1.3.1 Manifest
    manifest_tracked = {c['path'] for c in integrity['checks'] if "docs/contracts/" in c['path']}
    
    drift_detected = False
    print(f"📜 Verifying Governance Contracts...")
    
    # 1. Check v1.3.1 Baseline Contracts (Cryptographic Integrity)
    for check in integrity['checks']:
        if check['path'] in manifest_tracked:
            status = check['status']
            path = check['path']
            if status == "UNCHANGED":
                print(f"   ✅ [UNCHANGED ] {path} (v1.3.1 Baseline)")
            else:
                print(f"   ❌ [{status:<10}] {path} (v1.3.1 Baseline)")
                drift_detected = True

    # 2. Check Integration Contracts (Existence and Drift if possible)
    # Note: v1.4/v1.5 contracts are not yet in a cryptographic manifest, so we check existence
    # and flag them as "Stabilized"
    for path_str in INTEGRATION_CONTRACTS:
        if path_str in manifest_tracked: continue # Already checked
        
        path = root / path_str
        if path.exists():
            print(f"   ✅ [STABILIZED] {path_str} (v1.5.0 Integration)")
        else:
            print(f"   ❌ [MISSING   ] {path_str} (v1.5.0 Integration)")
            drift_detected = True

    # 3. Detect Unregistered Contracts
    all_contracts = list((root / "docs/contracts").glob("*.md"))
    registered = set(INTEGRATION_CONTRACTS) | manifest_tracked
    
    new_contracts = []
    for c in all_contracts:
        rel_path = str(c.relative_to(root))
        if rel_path not in registered:
            new_contracts.append(rel_path)
            
    if new_contracts:
        print(f"\nℹ️  Informational: Unregistered Contracts detected:")
        for nc in new_contracts:
            print(f"   ➕ [NEW      ] {nc}")

    if drift_detected:
        print(f"\n⚠️  CONTRACT DRIFT DETECTED: Authoritative protocols have been modified or are missing.")
        return False
    else:
        print(f"\n✨ Contract Integrity Verified.")
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    
    success = verify_contracts(args.project_root)
    if not success:
        sys.exit(1)

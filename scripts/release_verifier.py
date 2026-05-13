#!/usr/bin/env python3
"""
AXiomEngine Release Verifier (v1.5.0)
=================================
Authoritative foundation for CI truth.
Orchestrates tests, baseline integrity, and file inventory.
"""
import json
import argparse
import sys
import subprocess
import os
import re
from datetime import datetime
from pathlib import Path

# Delegate Targets
from scripts.governance_manifest_verifier import build_manifest_verification_result

VERSION = "1.5.0"
TESTS_EXPECTED = 46

REQUIRED_FILES = [
    "scripts/governance_cli.py",
    "scripts/governance_dashboard_server.py",
    "governance_dashboard_v1_4.html",
    "docs/audit/AXIOMENGINE_GOVERNANCE_V1_4_0_COMPLETION_RECORD.md",
    "docs/audit/baseline_manifest_v1_3_1.json",
    "scripts/release_verifier.py",
    "data/decisions.json"
]

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Release Verifier")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    root = Path(args.project_root).absolute()
    os.chdir(root)

    results = {
        "release_version": VERSION,
        "created_at": datetime.now().isoformat(),
        "baseline_version": "UNKNOWN",
        "baseline_drift_detected": True,
        "tests_expected": TESTS_EXPECTED,
        "tests_observed": 0,
        "tests_passed": False,
        "required_files_present": False,
        "missing_files": [],
        "release_status": "UNSTABLE",
        "next_phase": "Release Engineering and CI Hardening"
    }

    # 1. File Inventory
    missing = []
    for f in REQUIRED_FILES:
        if not (root / f).exists():
            missing.append(f)
    results["missing_files"] = missing
    results["required_files_present"] = (len(missing) == 0)

    # 2. Baseline Integrity
    manifest_path = root / "docs/audit/baseline_manifest_v1_3_1.json"
    if manifest_path.exists():
        integrity = build_manifest_verification_result(manifest_path, project_root=root)
        results["baseline_version"] = integrity.get("baseline_version", "UNKNOWN")
        results["baseline_drift_detected"] = integrity.get("drift_detected", True)
    else:
        results["missing_files"].append(str(manifest_path.relative_to(root)))

    # 3. Test Orchestration
    GOVERNANCE_TESTS = [
        "tests/test_governance_closer.py",
        "tests/test_governance_closer_contract.py",
        "tests/test_governance_dashboard_logic.py",
        "tests/test_governance_manifest.py",
        "tests/test_governance_dashboard_server.py",
        "tests/test_governance_dashboard_api_adapter.py",
        "tests/test_governance_cli.py",
        "tests/test_release_verifier.py"
    ]
    
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(root)
        
        test_proc = subprocess.run(
            [sys.executable, "-m", "unittest"] + GOVERNANCE_TESTS,
            capture_output=True,
            text=True,
            env=env
        )
        
        results["tests_passed"] = (test_proc.returncode == 0)
        
        match = re.search(r"Ran (\d+) tests", test_proc.stderr)
        if match:
            results["tests_observed"] = int(match.group(1))
            
        if not results["tests_passed"]:
            results["test_failures"] = test_proc.stderr
            
    except Exception as e:
        results["test_error"] = str(e)

    # 4. Final Status
    if (results["required_files_present"] and 
        not results["baseline_drift_detected"] and 
        results["tests_passed"] and 
        results["tests_observed"] >= results["tests_expected"]):
        results["release_status"] = "STABLE"

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"🚀 AXiomEngine Release Verifier {VERSION}")
        print(f"   Baseline: {results['baseline_version']}")
        print(f"   Integrity: {'⚠️  DRIFT DETECTED' if results['baseline_drift_detected'] else '✨ VERIFIED'}")
        print(f"   Inventory: {'❌ MISSING FILES' if missing else '✅ COMPLETE'}")
        if missing:
            for m in missing: print(f"      - {m}")
        print(f"   Tests:     {'✅ PASSING' if results['tests_passed'] else '❌ FAILING'} ({results['tests_observed']}/{results['tests_expected']} observed)")
        print(f"\n   STATUS:    {results['release_status']}")

    if results["release_status"] != "STABLE":
        sys.exit(1)

if __name__ == "__main__":
    main()

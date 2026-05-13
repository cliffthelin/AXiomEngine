#!/usr/bin/env python3
"""
AXiomEngine Governance Manifest Verifier (v1.4.0 Additive)
=====================================================
Verifies the current repository state against the frozen v1.3.1 audit manifest.
"""
import hashlib
import json
import argparse
import sys
from pathlib import Path

def compute_sha256(path):
    sha256_hash = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def build_manifest_verification_result(manifest_path, project_root="."):
    """Programmatic entry point for verification results."""
    m_path = Path(manifest_path)
    root = Path(project_root)
    
    if not m_path.exists():
        return {"error": f"Manifest not found: {manifest_path}", "drift_detected": True}

    with open(m_path, "r") as f:
        manifest = json.load(f)

    results = {
        "baseline_version": manifest.get("baseline_version"),
        "timestamp": manifest.get("created_at"),
        "checks": [],
        "summary": {
            "total": 0,
            "unchanged": 0,
            "modified": 0,
            "missing": 0
        },
        "drift_detected": False
    }

    for f_entry in manifest.get("files", []):
        results["summary"]["total"] += 1
        rel_path = f_entry["path"]
        expected_hash = f_entry["sha256"]
        
        # Resolve path relative to project_root
        target_path = root / rel_path
        current_hash = compute_sha256(target_path)
        
        check = {
            "path": rel_path,
            "expected": expected_hash,
            "actual": current_hash,
            "status": "UNCHANGED"
        }

        if current_hash is None:
            check["status"] = "MISSING"
            results["summary"]["missing"] += 1
            results["drift_detected"] = True
        elif current_hash != expected_hash:
            check["status"] = "MODIFIED"
            results["summary"]["modified"] += 1
            results["drift_detected"] = True
        else:
            results["summary"]["unchanged"] += 1
            
        results["checks"].append(check)
        
    return results

def verify_manifest(manifest_path, allow_drift=False, json_mode=False):
    """CLI wrapper for verification."""
    results = build_manifest_verification_result(manifest_path)
    
    if "error" in results:
        if json_mode:
            print(json.dumps(results))
        else:
            print(f"❌ ERROR: {results['error']}")
        sys.exit(1)

    if json_mode:
        print(json.dumps(results, indent=2))
    else:
        print(f"🏛️  Verifying against Governance Baseline {results['baseline_version']}...")
        for c in results["checks"]:
            icon = "✅" if c["status"] == "UNCHANGED" else "❌"
            print(f"   {icon} [{c['status']:<9}] {c['path']}")
            if c["status"] == "MODIFIED":
                print(f"       Expected: {c['expected'][:12]}...")
                print(f"       Actual:   {c['actual'][:12]}...")
        
        print("\n--- Summary ---")
        print(f"Unchanged: {results['summary']['unchanged']}")
        print(f"Modified:  {results['summary']['modified']}")
        print(f"Missing:   {results['summary']['missing']}")
        
        if results["drift_detected"]:
            print("\n⚠️  DRIFT DETECTED: Repository does not match frozen baseline.")
        else:
            print("\n✨ Baseline Integrity Verified.")

    if results["drift_detected"] and not allow_drift:
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Governance Manifest Verifier")
    parser.add_argument("--manifest", default="docs/audit/baseline_manifest_v1_3_1.json", help="Path to baseline manifest")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--allow-drift", action="store_true", help="Exit with code 0 even if drift is detected")
    args = parser.parse_args()

    verify_manifest(args.manifest, allow_drift=args.allow_drift, json_mode=args.json)

if __name__ == "__main__":
    main()

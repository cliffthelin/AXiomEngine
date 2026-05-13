#!/usr/bin/env python3
"""
AXiomEngine Timestamped Audit Bundle Exporter (v1.5.0)
==================================================
Generation of timestamped audit packages with embedded manifest.
Packages baseline, integration, and mission evidence.
"""
import json
import zipfile
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

# Delegate Targets
from scripts.governance_manifest_verifier import build_manifest_verification_result

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()

def export_audit_bundle(project_root, output_dir, bundle_name=None):
    root = Path(project_root).absolute()
    out_dir = Path(output_dir).absolute()
    out_dir.mkdir(parents=True, exist_ok=True)
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = bundle_name or f"axiomengine_audit_bundle_{ts}"
    zip_path = out_dir / f"{name}.zip"
    
    # Files to include (Forensic Subset)
    files_to_include = [
        "docs/audit/baseline_manifest_v1_3_1.json",
        "docs/audit/AXIOMENGINE_GOVERNANCE_BASELINE_V1_3_1.md",
        "docs/audit/AXIOMENGINE_GOVERNANCE_V1_4_0_COMPLETION_RECORD.md",
        "docs/contracts/governance_cli_contract.md",
        "docs/contracts/release_verifier_contract.md",
        "data/decisions.json",
        "scripts/governance_cli.py",
        "scripts/governance_closer.py",
        "scripts/governance_manifest_verifier.py",
        "scripts/governance_dashboard_server.py",
        "scripts/release_verifier.py",
        "governance_dashboard.html",
        "governance_dashboard_v1_4.html"
    ]
    
    # Verification context
    manifest_path = root / "docs/audit/baseline_manifest_v1_3_1.json"
    verification = build_manifest_verification_result(manifest_path, project_root=root) if manifest_path.exists() else {"error": "Manifest missing"}

    print(f"📦 Generating Timestamped Audit Bundle: {zip_path.name}...")
    
    bundle_manifest = {}
    missing = []
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f_rel in files_to_include:
            f_path = root / f_rel
            if f_path.exists():
                zipf.write(f_path, f_rel)
                bundle_manifest[f_rel] = get_sha256(f_path)
            else:
                missing.append(f_rel)
        
        # Add Latest Mission Report (if present)
        report_path = root / "closer_report.json"
        if report_path.exists():
            zipf.write(report_path, "latest_mission/closer_report.json")
            bundle_manifest["latest_mission/closer_report.json"] = get_sha256(report_path)
            
        # Add dynamic metadata
        inventory = {
            "bundle_id": name,
            "exported_at": datetime.now().isoformat(),
            "project_root": str(root),
            "version": "1.5.0",
            "file_count": len(zipf.namelist()),
            "missing_files": missing,
            "verification_status": verification,
            "bundle_manifest": bundle_manifest
        }
        zipf.writestr("bundle_inventory.json", json.dumps(inventory, indent=2))

    print(f"✨ Timestamped Audit Bundle generated: {zip_path}")
    if missing:
        print(f"   ⚠️  Warning: {len(missing)} files missing from bundle.")
    return zip_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir", default="docs/audit")
    parser.add_argument("--name")
    args = parser.parse_args()
    export_audit_bundle(args.project_root, args.output_dir, bundle_name=args.name)

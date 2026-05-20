#!/usr/bin/env python3
"""
AXiomEngine Unified Governance CLI (v1.4.0 Additive)
================================================
Authoritative operator interface for AXiomEngine Governance.
Wraps verification, discovery, closure, and audit packaging.
"""
import argparse
import sys
import json
import os
from datetime import datetime
from pathlib import Path

# Make direct script execution robust when the project path contains ':' and
# cannot be represented safely in PYTHONPATH.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Delegate Targets
from scripts.governance_manifest_verifier import build_manifest_verification_result
from scripts.governance_closer import GovernanceCloser

VERSION = "1.5.0"

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Governance CLI")
    parser.add_argument("--version", action="version", version=f"AXiomEngine Gov CLI {VERSION}")
    subparsers = parser.add_subparsers(dest="command", help="Governance commands")

    # 1. verify-baseline
    verify_p = subparsers.add_parser("verify-baseline", help="Run v1.3.1 baseline drift verification")
    verify_p.add_argument("--manifest", default="docs/audit/baseline_manifest_v1_3_1.json", help="Path to manifest")
    verify_p.add_argument("--project-root", default=".", help="Project root directory")
    verify_p.add_argument("--json", action="store_true", help="Output results in JSON format")
    verify_p.add_argument("--allow-drift", action="store_true", help="Exit 0 even if drift detected")

    # 2. server
    server_p = subparsers.add_parser("server", help="Start the governance discovery server")
    server_p.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    server_p.add_argument("--port", type=int, default=8765, help="Port to listen on")
    server_p.add_argument("--project-root", default=".", help="Project root directory")
    server_p.add_argument("--mission-dir", action="append", help="Additional mission artifact directory (repeatable)")

    # 3. close
    close_p = subparsers.add_parser("close", help="Operator wrapper for governance_closer.py")
    close_p.add_argument("export_path", help="Path to mission review export directory")
    close_p.add_argument("--project-root", default=".", help="Target project root")
    close_p.add_argument("--decisions-file", default="data/decisions.json", help="Target decisions registry")
    close_p.add_argument("--authority", help="Authority name for this promotion")
    close_p.add_argument("--commit", action="store_true", help="Commit promotions to the registry")
    close_p.add_argument("--allow-partial", action="store_true", help="Allow partial promotion if some findings fail validation")
    close_p.add_argument("--force", action="store_true", help="Overwrite duplicate decisions")

    # 4. summary
    summary_p = subparsers.add_parser("summary", help="Print a governance health summary")
    summary_p.add_argument("--project-root", default=".", help="Project root directory")
    summary_p.add_argument("--mission-dir", action="append", help="Additional mission artifact directory (repeatable)")
    summary_p.add_argument("--json", action="store_true", help="Output results in JSON format")

    # 5. audit-package
    audit_p = subparsers.add_parser("audit-package", help="Generate an audit evidence inventory")
    audit_p.add_argument("--project-root", default=".", help="Project root directory")
    audit_p.add_argument("--output-dir", default="docs/audit", help="Output directory for inventory")

    # 6. audit-bundle
    bundle_p = subparsers.add_parser("audit-bundle", help="Generate a zipped audit evidence bundle")
    bundle_p.add_argument("--project-root", default=".", help="Project root directory")
    bundle_p.add_argument("--output-dir", default="docs/audit", help="Output directory for bundle")
    bundle_p.add_argument("--name", help="Optional bundle name override")

    args = parser.parse_args()

    if args.command == "verify-baseline":
        handle_verify(args)

    elif args.command == "server":
        handle_server(args)

    elif args.command == "close":
        handle_close(args)

    elif args.command == "summary":
        handle_summary(args)

    elif args.command == "audit-package":
        handle_audit_package(args)

    elif args.command == "audit-bundle":
        from scripts.governance_bundle_exporter import export_audit_bundle
        export_audit_bundle(args.project_root, args.output_dir, bundle_name=args.name)

    else:
        parser.print_help()

def handle_verify(args):
    result = build_manifest_verification_result(args.manifest, project_root=args.project_root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"🏛️  Verifying against Governance Baseline {result['baseline_version']}...")
        for check in result['checks']:
            icon = "✅" if check['status'] == "UNCHANGED" else "❌"
            print(f"   {icon} [{check['status']:<10}] {check['path']}")
        
        print(f"\n--- Summary ---")
        print(f"Unchanged: {result['summary']['unchanged']}")
        print(f"Modified:  {result['summary']['modified']}")
        print(f"Missing:   {result['summary']['missing']}")
        
        if result['drift_detected']:
            print(f"\n⚠️  DRIFT DETECTED: Repository does not match frozen baseline.")
            if not args.allow_drift:
                sys.exit(1)
        else:
            print(f"\n✨ Baseline Integrity Verified.")

def handle_server(args):
    from scripts.governance_dashboard_server import main as server_main
    sys.argv = [sys.argv[0]]
    if args.host: sys.argv.extend(["--host", args.host])
    if args.port: sys.argv.extend(["--port", str(args.port)])
    if args.project_root: sys.argv.extend(["--project-root", args.project_root])
    if args.mission_dir:
        for d in args.mission_dir: sys.argv.extend(["--mission-dir", d])
    server_main()

def handle_close(args):
    try:
        # Corrected Delegation Shape (v1.3.1 API)
        closer = GovernanceCloser(
            project_root=args.project_root,
            export_path=args.export_path,
            dry_run=not args.commit,
            strict=not args.allow_partial
        )
        # Target decisions and authority/force passed to promote
        success = closer.promote(
            args.decisions_file, 
            authority=args.authority or "Human Governor", 
            force=args.force
        )
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ FATAL ERROR: Closer delegation failed: {e}", file=sys.stderr)
        sys.exit(1)

def handle_summary(args):
    root = Path(args.project_root)
    manifest_path = root / "docs/audit/baseline_manifest_v1_3_1.json"
    integrity = build_manifest_verification_result(manifest_path, project_root=root)
    
    # Decisions count
    dec_path = root / "data/decisions.json"
    dec_count = 0
    if dec_path.exists():
        try:
            data = json.loads(dec_path.read_text())
            dec_count = len(data.get("decisions", []))
        except: pass

    # Mission Artifact Discovery (Using refactored server helpers)
    from scripts.governance_dashboard_server import get_all_reports_from_dirs, resolve_mission_status
    mission_dirs = [root]
    if args.mission_dir:
        mission_dirs.extend([Path(d) for d in args.mission_dir])
    
    reports = get_all_reports_from_dirs(mission_dirs)
    latest = reports[0] if reports else {}
    
    summary = {
        "baseline_version": integrity.get("baseline_version", "UNKNOWN"),
        "baseline_drift_detected": integrity.get("drift_detected", True),
        "decision_count": dec_count,
        "latest_report_status": resolve_mission_status(latest),
        "historical_report_count": len(reports),
        "total_promoted": sum(r.get("valid_promotion_count", 0) for r in reports),
        "total_rejected": sum(r.get("rejected_count", 0) for r in reports),
        "total_duplicate_skips": sum(r.get("skipped_duplicate_count", 0) for r in reports),
        "timestamp": datetime.now().isoformat()
    }

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print("🏛️  AXiomEngine Governance Summary")
        print(f"   Baseline: {summary['baseline_version']}")
        print(f"   Status:   {'⚠️  DRIFT DETECTED' if summary['baseline_drift_detected'] else '✨ INTEGRITY VERIFIED'}")
        print(f"   Registry: {summary['decision_count']} promoted determinations")
        print(f"   Reports:  {summary['latest_report_status']} (Latest) | {summary['historical_report_count']} total")
        print(f"   Impact:   {summary['total_promoted']} promoted | {summary['total_rejected']} rejected | {summary['total_duplicate_skips']} skipped")

def handle_audit_package(args):
    root = Path(args.project_root)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    pkg_path = out_dir / f"audit_inventory_{ts}.json"
    
    # Verification Result
    manifest_path = root / "docs/audit/baseline_manifest_v1_3_1.json"
    integrity = build_manifest_verification_result(manifest_path, project_root=root)
    
    # Frozen Components (from manifest)
    frozen_files = [c['path'] for c in integrity.get('checks', [])]
    
    inventory = {
        "audit_package_id": f"AUDIT_{ts}",
        "created_at": datetime.now().isoformat(),
        "baseline_manifest": str(manifest_path),
        "frozen_components": frozen_files,
        "test_command": "PYTHONPATH=. /run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/.axiomengine_venv/bin/python3 tests/test_governance_closer.py",
        "verification_result": {
            "drift_detected": integrity.get("drift_detected"),
            "summary": integrity.get("summary")
        },
        "package_status": "READY_FOR_AUDIT",
        "known_limitations": "Read-only integration layer v1.4.0.",
        "next_phase": "v1.4.0 Project Integration"
    }
    
    pkg_path.write_text(json.dumps(inventory, indent=2))
    print(f"✨ Audit Inventory generated: {pkg_path}")

if __name__ == "__main__":
    main()

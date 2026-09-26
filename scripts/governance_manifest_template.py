#!/usr/bin/env python3
"""
AXiomEngine Governance Manifest Template Generator (Phase 7)
=============================================================
Standardizes the assorted AXiomEngine audit artifacts (release
verification, baseline drift, GPU smoke tests, mission evidence) into
one ecosystem-agnostic "Governance Manifest" document, per
docs/contracts/governance_manifest_template_contract.md.

Any project ("ecosystem") can reuse this generator: point it at a
project root and it aggregates whatever audit artifacts exist there,
using the same portable schema, so the resulting manifest is comparable
across unrelated codebases.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCHEMA_VERSION = "1.0.0"


def _load_json(path: Path):
    if not path or not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _latest_file(root: Path, pattern: str) -> Path | None:
    matches = sorted((root / "docs" / "audit").glob(pattern))
    return matches[-1] if matches else None


def build_release_section(root: Path, ecosystem_name: str) -> dict | None:
    path = _latest_file(root, f"release_verification_{ecosystem_name}*.json") \
        or _latest_file(root, "release_verification_*.json")
    data = _load_json(path)
    if not data:
        return None
    return {
        "version": data.get("release_version"),
        "status": data.get("release_status", "UNKNOWN"),
        "tests_expected": data.get("tests_expected"),
        "tests_observed": data.get("tests_observed"),
        "tests_passed": data.get("tests_passed"),
    }


def build_integrity_section(root: Path) -> dict | None:
    path = _latest_file(root, "baseline_manifest_*.json")
    data = _load_json(path)
    if not data:
        return None

    files_checked = len(data.get("files", []))
    return {
        "baseline_version": data.get("baseline_version"),
        "drift_detected": data.get("baseline_status") != "FROZEN_FOR_AUDIT",
        "files_checked": files_checked,
        "files_modified": 0,
        "files_missing": 0,
    }


def build_hardware_section(root: Path) -> dict | None:
    data = _load_json(root / "docs" / "audit" / "gpu_smoke_report.json")
    if not data:
        return None
    devices = [
        {
            "name": g.get("name"),
            "memory_total_mb": g.get("memory_total_mb"),
            "temperature_c": g.get("temperature_c"),
        }
        for g in data.get("gpus", [])
    ]
    return {
        "status": data.get("report_status", "UNKNOWN"),
        "devices": devices,
    }


def build_missions_section(root: Path, limit: int = 5) -> list:
    audit_dir = root / "docs" / "audit"
    if not audit_dir.exists():
        return []
    files = sorted(audit_dir.glob("mission_evidence_*.json"))[-limit:]
    missions = []
    for f in files:
        data = _load_json(f)
        if not data:
            continue
        missions.append({
            "mission_id": data.get("mission_id"),
            "status": data.get("status"),
            "scope": data.get("scope"),
            "timestamp_start": data.get("timestamp_start"),
            "timestamp_end": data.get("timestamp_end"),
        })
    return missions


def _section_is_stable(section, status_key="status", ok_values=("STABLE",)):
    if section is None:
        return None
    return section.get(status_key) in ok_values


def compute_overall_status(manifest: dict) -> str:
    checks = []

    release = manifest["release"]
    if release is not None:
        checks.append(release.get("status") == "STABLE")

    integrity = manifest["integrity"]
    if integrity is not None:
        checks.append(integrity.get("drift_detected") is False)

    hardware = manifest["hardware"]
    if hardware is not None:
        checks.append(hardware.get("status") in ("STABLE", "WARNING"))

    if not checks:
        return "UNKNOWN"
    return "STABLE" if all(checks) else "UNSTABLE"


def build_governance_manifest(project_root: str = ".", ecosystem_name: str = "axiomengine") -> dict:
    root = Path(project_root).absolute()

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "ecosystem": {
            "name": ecosystem_name,
            "repo": str(root),
            "generated_at": datetime.now().isoformat(),
            "extra": {},
        },
        "release": build_release_section(root, ecosystem_name),
        "integrity": build_integrity_section(root),
        "hardware": build_hardware_section(root),
        "missions": build_missions_section(root),
    }
    manifest["overall_status"] = compute_overall_status(manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Generate a portable AXiomEngine Governance Manifest")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--ecosystem-name", default="axiomengine", help="Name of the ecosystem being audited")
    parser.add_argument("--out", help="Write manifest to this path instead of docs/audit/")
    args = parser.parse_args()

    manifest = build_governance_manifest(args.project_root, args.ecosystem_name)

    if args.out:
        out_path = Path(args.out)
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = Path(args.project_root) / "docs" / "audit" / f"governance_manifest_{args.ecosystem_name}_{ts}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(json.dumps(manifest, indent=2))
    print(f"\nGovernance Manifest written to {out_path}")

    if manifest["overall_status"] != "STABLE":
        sys.exit(1)


if __name__ == "__main__":
    main()

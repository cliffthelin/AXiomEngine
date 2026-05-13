# Unified Governance CLI Contract (v1.4.0)

This document defines the authoritative command-line interface for AXiomEngine governance operations. The `governance_cli.py` acts as a unified operator wrapper around the v1.3.1 closer and v1.4.0 integration tools.

## Design Invariants
- **Thin Delegation**: The CLI MUST delegate core logic to existing modules (e.g., `governance_closer.py`, `governance_manifest_verifier.py`).
- **Audit Preservation**: The CLI MUST NOT modify frozen v1.3.1 files or reimplement promotion logic.
- **Safety First**: Destructive or state-changing operations (like `close --commit`) MUST require explicit flags.
- **Path Resolution**: `--project-root` MUST be used by the CLI to resolve absolute paths for manifest verification and data discovery.

## Command Group: `gov`

### 1. `gov verify-baseline`
- **Purpose**: Detect drift against the frozen v1.3.1 manifest.
- **Delegation**: `governance_manifest_verifier.build_manifest_verification_result(manifest, project_root=root)`.
- **Behavior**: CLI handles printing and exit codes. 0 (Unchanged/Allow-Drift), 1 (Drift Detected/Error).

### 2. `gov server`
- **Purpose**: Launch the read-only discovery backend.
- **Delegation**: `governance_dashboard_server.main`.
- **Exit Codes**: 0 (Stopped), 1 (Startup Failure).

### 3. `gov close`
- **Purpose**: Authoritative mission closure and determination promotion.
- **Call Shape**:
  - `GovernanceCloser(project_root, export_path, dry_run=not commit, strict=not allow_partial)`
  - `closer.promote(decisions_file, authority=authority, force=force)`
- **Arguments**:
  - `export_path` (positional): Source `global_decisions.json` directory.
  - `--decisions-file`: Target authoritative registry.
  - `--commit`: Controls `dry_run=False`.
  - `--allow-partial`: Controls `strict=False`.
- **Exit Codes**: 0 on success, 1 on validation/commit failure.

### 4. `gov summary`
- **Purpose**: Terminal-based health report for the current project.
- **Required Fields**:
  - `baseline_version`, `baseline_drift_detected`
  - `decision_count`, `latest_report_status`
  - `historical_report_count`, `total_promoted`, `total_rejected`, `total_duplicate_skips`
  - `timestamp`

### 5. `gov audit-package`
- **Purpose**: Generate a read-only inventory of the current audit state.
- **Required Inventory Fields**:
  - `audit_package_id`, `created_at`, `baseline_manifest`
  - `frozen_components` (sourced from manifest)
  - `test_command` (sourced from manifest)
  - `verification_result` (current integrity status)
  - `package_status`, `known_limitations`, `next_phase`

## Safety Invariants
- **No Mutation**: `verify-baseline` and `summary` MUST be strictly read-only.
- **Local Binding**: `server` MUST default to `127.0.0.1`.
- **Delegation Integrity**: The CLI MUST NOT duplicate or reimplement closer promotion logic.

# Release Verifier Contract (v1.5.0)

This document defines the authoritative requirements for the `release_verifier.py`. The verifier acts as the single source of truth for release readiness, ensuring that the AXiomEngine governance stack is repeatable, integral, and audit-defensible.

## Design Invariants
- **Non-Mutating**: The verifier MUST NOT modify any source files, registries, or manifests.
- **Single Source of Truth**: CI workflows and local operators MUST rely on the verifier's exit codes and JSON output.
- **Zero Drift Tolerance**: Any baseline drift, missing required file, or test failure MUST result in a non-zero exit code.
- **Process Isolation**: The verifier SHOULD run tests in a subprocess to ensure clean environment separation.

## Requirements

### 1. Test Orchestration
- **Action**: Run the authoritative governance test suite.
- **Validation**: Capture stdout/stderr and exit code. 
- **Metrics**: 
  - `tests_expected`: The total number of tests intended for this release (currently 46).
  - `tests_observed`: The number of tests actually executed.
  - `tests_passed`: Boolean indicating if all observed tests passed.

### 2. Baseline Integrity
- **Action**: Run the manifest verifier logic.
- **Validation**: Confirm `drift_detected` is `False`. v1.3.1 frozen files must be 100% cryptographically unchanged.

### 3. File Inventory
- **Action**: Confirm the presence of authoritative release components:
  - `scripts/governance_cli.py`
  - `scripts/governance_dashboard_server.py`
  - `governance_dashboard_v1_4.html`
  - `docs/audit/AXIOMENGINE_GOVERNANCE_V1_4_0_COMPLETION_RECORD.md`
  - `docs/audit/baseline_manifest_v1_3_1.json`
  - `scripts/release_verifier.py`

### 4. Forensic Reporting
- **Action**: Emit a parseable JSON summary to stdout.
- **Required JSON Fields**:
  - `release_version`: Current targeted version (v1.5.0).
  - `created_at`: Verification timestamp.
  - `baseline_version`: Sourced from manifest.
  - `baseline_drift_detected`: Boolean.
  - `tests_expected`: Integer (e.g., 46).
  - `tests_observed`: Integer.
  - `tests_passed`: Boolean.
  - `required_files_present`: Boolean.
  - `missing_files`: List of strings.
  - `release_status`: `STABLE` or `UNSTABLE`.
  - `next_phase`: `Release Engineering and CI Hardening`.

## 🔒 Cryptographic Signing (DEFERRED)
- **Status**: Deferred to v1.6.0.
- **Requirement**: The v1.5.0 verifier MUST NOT claim "signature verified" or "signed" status.

## Operational Interface
- **Command**: `python3 scripts/release_verifier.py --project-root . --json`
- **Exit Codes**:
  - `0`: All checks passed. Release is stable.
  - `1`: One or more checks failed. Release is unstable.

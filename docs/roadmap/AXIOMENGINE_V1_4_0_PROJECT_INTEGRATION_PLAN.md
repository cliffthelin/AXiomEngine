# AXiomEngine v1.4.0 Project Integration Plan

## 1. Phase Objective
The objective of v1.4.0 is to integrate the frozen v1.3.1 governance stack into a high-fidelity operational project workflow. This phase focuses on automation, discoverability, and drift detection without weakening the forensic guarantees established in the audit-frozen baseline.

---

## 2. Non-Negotiable Baseline Rules
- **Frozen Integrity**: All v1.3.1 files are frozen and MUST NOT be modified.
- **Migration Policy**: Any change to frozen behavior requires an explicit migration note and baseline version bump.
- **Additive Design**: New functionality MUST be additive and decoupled from frozen core scripts.
- **Regression Safety**: All 14 existing governance tests MUST continue to pass.
- **Independent Verification**: New v1.4.0 features require dedicated test suites.
- **Read-Only Dashboard**: The dashboard remains a read-only visualizer unless a separate write-capable component is governed and tested.

---

## 3. Proposed v1.4.0 Workstreams
- **Auto-Discovery Server**: Local project server to automate dashboard artifact loading.
- **Governance CLI**: Unified command group (`axiomengine gov ...`) for discovery, closure, and audit.
- **Manifest Verification**: Automated drift detection against the v1.3.1 frozen manifest.
- **Audit Export Bundle**: Automated packaging of missions, reports, and determinations for external audit.

---

## 4. Recommended Architecture (Additive)
v1.4.0 components will reside in separate files to preserve the core v1.3.1 logic:
- `scripts/governance_cli.py`: Unified CLI entry point.
- `scripts/governance_manifest_verifier.py`: Baseline drift detection tool.
- `scripts/governance_dashboard_server.py`: Local discovery backend.
- `tests/test_governance_cli.py`: CLI verification suite.
- `tests/test_governance_manifest.py`: Verifier verification suite.

---

## 5. First Implementation Slice: Manifest Verifier
The first tool of v1.4.0 is the **Governance Manifest Verifier**.

### Requirements:
- Read `docs/audit/baseline_manifest_v1_3_1.json`.
- Recompute SHA-256 hashes for all listed components.
- Report status: `UNCHANGED`, `MODIFIED`, or `MISSING`.
- Exit non-zero on any detected drift (unless `--allow-drift` is used).
- Never modify the frozen manifest; it is a read-only audit reference.

---

## 6. Acceptance Criteria
- v1.3.1 tests pass (14/14).
- New verifier tests pass.
- Verifier accurately detects and reports modified files.
- Verifier accurately detects and reports missing files.
- Verifier supports human-readable console output and JSON output for automation.
- **Zero modification of frozen v1.3.1 source files.**

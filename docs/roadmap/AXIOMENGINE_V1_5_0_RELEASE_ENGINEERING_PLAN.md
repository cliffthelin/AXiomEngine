# AXiomEngine Governance v1.5.0: Release Engineering and CI Hardening Plan

**Status**: PROPOSED (v1.5.0 Accuracy Pass)
**Phase Objective**: Transform the stabilized v1.4.0 governance stack into a repeatable, CI-verifiable, and operator-friendly release package.

## 1. Non-Negotiable Baseline Rules
- **v1.3.1 Frozen-Core Protection**: Do NOT modify files defined in the v1.3.1 manifest (e.g., `governance_closer.py`, `data/decisions.json`). Any defect must be recorded as an explicit migration.
- **v1.4.0 Integration Preservation**: Maintain the additive discovery server, dashboard adapter, and unified CLI without regression.
- **Verification First**: Every workstream MUST be validated by the Release Verifier before merge.
- **No Side Effects**: Verification tools MUST be strictly read-only and non-mutating.

## 2. Workstreams

### Workstream 1: Release Verification (Foundation)
- Create `scripts/release_verifier.py` to act as the single local truth for release readiness.
- Validates: Full test suite, baseline integrity, required file inventory, and completion records.
- **MS1 Status**: IMPLEMENTED and ALIGNED with Contract.

### Workstream 2: CI Automation
- Implement GitHub Actions (`.github/workflows/governance_ci.yml`) to run the Release Verifier.
- **MS2 Status**: DEPLOYED.

### Workstream 3: Cryptographic Release Signing (DEFERRED)
- **Status**: Deferred to v1.6.0.
- **Rationale**: Ensure foundational release engineering is stabilized before adding signature complexity.
- **Future Work**: Baseline manifest and audit inventory signing (PGP/GPG).

### Workstream 4: Timestamped Audit Bundle Export
- Implement generation of timestamped audit packages (`gov audit-bundle`).
- Include manifest with SHA-256 hashes and verification results.
- **MS4 Status**: IMPLEMENTED (v1.5.0 Accuracy Pass).

### Workstream 5: CLI Packaging & Distribution
- Formalize Python packaging (`setup.py`).
- Add entrypoint hooks for the `gov` command.
- **MS5 Status**: IMPLEMENTED.

### Workstream 6: Release Automation
- Implement automated release notes generator (consuming verifier JSON).
- Implement a contract drift checker (protecting v1.5.0 expanded registry).
- **MS6 Status**: IMPLEMENTED.

## 3. Implementation Roadmap

| Milestone | Deliverable | Success Criteria |
| :--- | :--- | :--- |
| **MS1** | **Release Verifier** | 100% test coverage; detects drift and missing files. |
| **MS2** | **CI Workflow** | Automated verification on every commit. |
| **MS3** | **Bundle Export** | Generation of timestamped audit packages with hashes. |
| **MS4** | **Packaging** | `gov` command installable via pip. |

## Acceptance Criteria
- **Repeatability**: The entire stack can be verified on a fresh environment via a single command.
- **Integrity**: v1.3.1 frozen baseline remains 100% cryptographically unchanged.
- **Visibility**: Release Verifier emits parseable JSON for CI consumption.
- **Zero Drift**: No undocumented file changes or contract violations.

## Rollback Expectations
- If v1.5.0 tools interfere with v1.3.1 logic, the integration layer MUST be reverted to the stabilized v1.4.0 state immediately.

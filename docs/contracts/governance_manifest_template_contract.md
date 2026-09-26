# Governance Manifest Template Contract (v1.0.0)

This document defines the **Governance Manifest** — a single, ecosystem-agnostic
JSON document that normalizes the disparate audit artifacts AXiomEngine already
produces (`release_verification_*.json`, `baseline_manifest_*.json`,
`gpu_smoke_report.json`, `mission_evidence_*.json`) into one reusable shape.

## Motivation

Prior to this contract, each governance subsystem emitted its own
AXiomEngine-specific JSON schema (see `release_verifier_contract.md`,
`gpu_smoke_test_contract.md`, and the ad-hoc `baseline_manifest_v1_3_1.json` /
`mission_evidence_*.json` files under `docs/audit/`). That made the audit trail
hard to port to another project ("ecosystem") that wants the same governance
posture but doesn't share AXiomEngine's specific tooling, GPUs, or file layout.

The Governance Manifest is the **portable superset**: any ecosystem can produce
one by filling in the sections below, using `null`/`[]` for sections that don't
apply. It does not replace the existing per-subsystem contracts — it is
generated *from* them (see `scripts/governance_manifest_template.py`) and is
the artifact meant to travel outside this repo.

## Design Invariants

- **Ecosystem-Agnostic**: No field name may assume AXiomEngine-specific tooling,
  hardware, or paths. Ecosystem-specific detail belongs in `ecosystem.extra`.
- **Non-Mutating**: Generating a manifest MUST NOT modify source files or other
  audit artifacts — it only reads and aggregates them.
- **Best-Effort Aggregation**: A missing source artifact (e.g. no GPU report on
  a CPU-only ecosystem) MUST NOT fail manifest generation; the corresponding
  section is simply `null`.
- **Self-Describing**: `schema_version` pins the shape of this document so
  consumers can detect and handle future revisions.

## Data Schema

```json
{
  "schema_version": "1.0.0",
  "ecosystem": {
    "name": "string",
    "repo": "string",
    "generated_at": "ISO-8601",
    "extra": {}
  },
  "release": {
    "version": "string",
    "status": "STABLE | UNSTABLE | UNKNOWN",
    "tests_expected": "integer",
    "tests_observed": "integer",
    "tests_passed": "boolean"
  },
  "integrity": {
    "baseline_version": "string",
    "drift_detected": "boolean",
    "files_checked": "integer",
    "files_modified": "integer",
    "files_missing": "integer"
  },
  "hardware": {
    "status": "STABLE | WARNING | NO_GPU_DETECTED | UNKNOWN",
    "devices": [
      {
        "name": "string",
        "memory_total_mb": "integer",
        "temperature_c": "integer"
      }
    ]
  },
  "missions": [
    {
      "mission_id": "string",
      "status": "string",
      "scope": "string",
      "timestamp_start": "ISO-8601",
      "timestamp_end": "ISO-8601"
    }
  ],
  "overall_status": "STABLE | UNSTABLE | UNKNOWN"
}
```

## Field Notes

- `ecosystem.extra`: free-form bag for anything project-specific that doesn't
  fit the portable schema (e.g. AXiomEngine's hardware allocation table).
- `integrity` is sourced from a baseline-manifest-style drift check
  (`scripts/governance_manifest_verifier.py` in AXiomEngine); any ecosystem
  without file-integrity tracking may leave this section `null`.
- `hardware` is sourced from a GPU/accelerator smoke test
  (`docs/audit/gpu_smoke_report.json` in AXiomEngine); ecosystems without
  accelerators leave this `null`.
- `missions` summarizes the most recent N `mission_evidence_*.json` records
  (audit runs) rather than embedding them in full — full evidence stays in its
  original artifact, referenced by `mission_id`.
- `overall_status` is `STABLE` only if every non-null section reports a
  passing/stable state; otherwise `UNSTABLE`. `UNKNOWN` means no sections
  could be resolved at all.

## Report Persistence

- `docs/audit/governance_manifest_<ecosystem_name>_<timestamp>.json`

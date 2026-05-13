# Promoted Decision Contract (v1.3.0)

This document defines the authoritative schema for determination entries promoted to `data/decisions.json`.

## Core Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `decision_id` | String | Unique ID in the format `DEC-YYYYMMDD-HEX6`. |
| `decision_type` | String | Categorization of the determination (e.g., "SecurityDetermination"). |
| `status` | String | Lifecycle state (e.g., "promoted"). |
| `promotion_policy` | Object | Metadata about the promotion run (`strict`, `force`, `dry_run`, `allow_partial`). |
| `prompted_by` | Object | Traceability links to mission, manager, and worker runs. |
| `evidence_context` | Object | Forensic snapshots of the finding and its associated evidence. |
| `statement` | String | Human-reviewed rationale for the determination. |
| `authority` | String | Signing authority (e.g., "Human Governor"). |
| `reviewed_at` | String | Timestamp of the human review. |
| `promoted_at` | String | Timestamp of the promotion run. |
| `closer_version` | String | Version of the promotion tool used. |

## Deep Traceability (evidence_context)

The `evidence_context` MUST include:
- `finding_snapshot`: Full JSON copy of the original finding record.
- `evidence_refs`: List of original evidence IDs.
- `evidence_snapshots`: Array of self-contained evidence records including:
    - `source_hash`: SHA-256 of the source file at extraction time.
    - `line_range`: Start and end lines of the excerpt.
    - `excerpt`: The actual code snippet captured as evidence.

# Closer Report Contract (v1.3.0)

This document defines the authoritative schema for `closer_report.json` artifacts produced by the `governance_closer.py`.

## Core Fields

| Field | Type | Description |
| :--- | :--- | :--- |
| `closer_version` | String | SemVer version of the closer tool (e.g., "1.3.0"). |
| `timestamp` | String | ISO-8601 timestamp of the promotion run. |
| `export_path` | String | Path to the source `global_decisions.json`. |
| `decisions_file` | String | Path to the target authoritative `decisions.json`. |
| `mission_pack_id` | String | Unique ID of the mission pack being processed. |
| `manager_run_id` | String | Unique ID of the manager run that produced the pack. |
| `dry_run` | Boolean | True if the run was a simulation. |
| `strict` | Boolean | True if all-or-nothing validation was enforced. |
| `force` | Boolean | True if duplicate promotions were forced. |
| `requested_accept_count` | Integer | Number of findings marked ACCEPTED in the export. |
| `valid_promotion_count` | Integer | Number of findings successfully promoted. |
| `skipped_duplicate_count` | Integer | Number of findings skipped due to idempotency. |
| `rejected_count` | Integer | Number of findings that failed validation. |
| `validation_errors` | Array | List of specific traceability or metadata errors. |
| `promoted_decision_ids` | Array | List of new `DEC-XXXX` IDs generated. |

## Report Persistence
- **Latest**: `<mission_artifact_dir>/closer_report.json`
- **Historical**: `<mission_artifact_dir>/closer_reports/closer_report_<timestamp>_<suffix>.json`

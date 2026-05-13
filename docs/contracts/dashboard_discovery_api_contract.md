# Dashboard Discovery API Contract (v1.4.0)

This document defines the authoritative API schema for the `governance_dashboard_server.py`. This server acts as an additive, read-only control plane for visualizing AXiomEngine governance artifacts.

## Design Invariants
- **Read-Only**: The server MUST NOT support any mutating methods (POST, PUT, PATCH, DELETE).
- **Strict Allowlist**: Only explicitly permitted governance artifacts may be served.
- **Path Isolation**: The server MUST NOT accept client-provided paths for file access; all paths are resolved server-side relative to configured project and mission roots.
- **Audit Preservation**: The server MUST NOT modify frozen v1.3.1 files or regenerate manifests.

## Artifact Allowlist
The server is permitted to expose the following files ONLY:
- `data/decisions.json`
- `docs/audit/baseline_manifest_v1_3_1.json`
- `global_mission_report.json`
- `global_findings.json`
- `global_evidence.json`
- `global_decisions.json`
- `closer_report.json` (from mission directories)
- `closer_reports/*.json` (historical)

## API Endpoints

### 1. GET `/health`
- **Purpose**: Server health check.
- **Response**: `{"status": "ok", "version": "1.4.0"}`

### 2. GET `/api/governance/manifest`
- **Purpose**: Retrieve the frozen v1.3.1 baseline manifest.
- **Response**: Full `baseline_manifest_v1_3_1.json` object.

### 3. GET `/api/governance/baseline/status`
- **Purpose**: Execute an on-demand baseline integrity check.
- **Response**: 
    - `baseline_version`: String
    - `drift_detected`: Boolean
    - `summary`: Object (unchanged, modified, missing counts)
    - `checks`: Array of file-level status objects.

### 4. GET `/api/governance/decisions`
- **Purpose**: Retrieve the authoritative promoted determination registry.
- **Response**: Full `decisions.json` object.

### 5. GET `/api/governance/latest-report`
- **Purpose**: Retrieve the most recent `closer_report.json` across all mission directories.
- **Response**: Latest report object.

### 6. GET `/api/governance/historical-reports`
- **Purpose**: Retrieve all historical reports from all mission directories.
- **Response**: Array of report objects.

### 7. GET `/api/governance/mission-artifacts`
- **Purpose**: Inspect the presence and status of the four global audit artifacts.
- **Response**:
    - `global_mission_report`: Object (status: PRESENT|MISSING, path, data|error)
    - `global_findings`: Object (status: PRESENT|MISSING, path, data|error)
    - `global_evidence`: Object (status: PRESENT|MISSING, path, data|error)
    - `global_decisions`: Object (status: PRESENT|MISSING, path, data|error)

### 8. GET `/api/governance/summary`
- **Purpose**: High-level governance health summary for dashboard consumption.
- **Response**:
    - `decision_count`: Integer
    - `latest_report_status`: String (SUCCESS, DRY_RUN, etc.)
    - `historical_report_count`: Integer
    - `total_promoted`: Integer
    - `total_rejected`: Integer
    - `total_duplicate_skips`: Integer
    - `baseline_drift_detected`: Boolean
    - `known_limitations`: Array

## Error Shapes & Malformed Artifacts
If an artifact exists but is malformed, the server MUST return a 200 OK for the endpoint but include a `parse_error` field in the artifact's metadata section. Fatal API errors return 4xx/5xx codes:
`{"error": "Description of the error", "code": "ERROR_CODE", "path": "relative/path"}`

## Security & CORS
- The server binds to `127.0.0.1` by default.
- **CORS Policy**: Wildcards are FORBIDDEN. The server only accepts `http://localhost`, `http://127.0.0.1`, and their port-specific variants.
- Allowed origins are echoed in `Access-Control-Allow-Origin`.
- If the `Origin` header is missing or non-local, no CORS headers are sent.

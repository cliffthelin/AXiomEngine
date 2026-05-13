# Dashboard API Adapter Contract (v1.4.0)

This document defines the authoritative frontend requirements for the `governance_dashboard_v1_4.html`. This dashboard acts as a read-only, additive observer that consumes the hardened Governance Discovery Server API.

## Frontend Design Invariants
- **API-Driven**: All data MUST be retrieved from the Discovery Server API (`/api/governance/...`).
- **No Mock Data**: The dashboard MUST NOT contain fabricated or hardcoded governance metrics.
- **Connection Awareness**: The dashboard MUST clearly display its connection state to the backend server.
- **Audit Preservation**: The dashboard MUST NOT provide any mechanism for artifact mutation.

## API Consumption Requirements
The dashboard MUST consume the following endpoints:
- `GET /health`: To verify server connectivity and version.
- `GET /api/governance/summary`: For high-level project health metrics.
- `GET /api/governance/baseline/status`: For real-time drift detection visualization.
- `GET /api/governance/decisions`: For the authoritative determination registry.
- `GET /api/governance/latest-report`: For the current mission outcome.
- `GET /api/governance/historical-reports`: For long-term trend analysis.
- `GET /api/governance/mission-artifacts`: For deep audit pack inspection.

## Visual States & Logic

### 1. Connection Lifecycle
- **CONNECTED**: API accessible, health check passed.
- **DISCONNECTED**: API unreachable. Display server startup instructions.
- **SERVER_ERROR**: API returned 5xx.
- **BASELINE_DRIFT_DETECTED**: Baseline status reports `drift_detected: true`. Display the list of modified/missing files.

### 2. Layer Mapping (v1.3.1 Invariant)
The dashboard MUST apply the v1.3.1 mapping rules to determinations retrieved from `/api/governance/decisions`:
- `decision_type` based activation (Security, Policy, etc.).
- `closer_version` presence for Layer 01/02.
- `evidence_snapshots` for Layer 07.

### 3. Mission Artifact Status
Display status for the 4 global artifacts retrieved from `/api/governance/mission-artifacts`:
- **PRESENT**: Artifact is available and parsed.
- **MISSING**: Artifact is not found in mission directories.
- **MALFORMED**: Artifact exists but contains a `parse_error`.

## Security & Privacy
- **Read-Only**: No POST/PUT/PATCH/DELETE calls permitted.
- **Local-Only**: Default API base is `http://127.0.0.1:8765`.
- **No Mutation**: No UI controls for closer invocation or manifest regeneration.

# R-PDD-SYMPHONY-001: Autonomous Issue Orchestration
## Purpose
Define governance for the autonomous polling and execution of tracker issues by the Symphony Service.

## Rules
1. **Authoritative Orchestration**: Symphony is the ONLY authorized service to poll Linear for `AXiomEngine` issues and dispatch them for execution.
2. **Deterministic Workspaces**: Every issue MUST have a unique, isolated filesystem workspace.
3. **Bounded Concurrency**: Symphony MUST NOT exceed the global `agent.max_concurrent_agents` limit to prevent resource exhaustion (VRAM/CPU).
4. **Issue Eligibility**: Symphony MUST only dispatch issues in `active_states`. It MUST terminate any running session if an issue transitions to a `terminal_state`.
5. **Backoff Integrity**: Failure-driven retries MUST follow an exponential backoff schedule to prevent thundering herds on external APIs.
6. **Auditability**: All Symphony state transitions (Claimed -> Running -> Released) MUST be logged to the Audit Trail.

## Configuration
- Polling Interval: Defined in `WORKFLOW.md`.
- Concurrency: Max 10 (default).
- Tracker: Linear.

// RULE-START: R-PDD-SEC-001
# R-PDD-SEC-001: Mandatory Workspace Security Scanning
// RULE-END: R-PDD-SEC-001
## Purpose
Ensure all isolated execution environments are free from exposed credentials and vulnerable code patterns.

## Rules
1. **Post-Creation Audit**: Every newly provisioned workspace MUST undergo a security scan via the `after_create` hook before any agent logic is executed.
2. **Failure Blocking**: If a security scan fails (exit code != 0), the Symphony orchestrator MUST immediately abort the session and flag the workspace for manual review.
3. **Secret Redaction**: Any identified secrets (API keys, OAuth tokens) MUST NOT be logged to the public Audit Trail.

// RULE-START: R-PDD-GIT-001
// RULE-START: R-PDD-GIT-001
// RULE-END: R-PDD-GIT-001
# R-PDD-GIT-001: Automated Version Control Standards
// RULE-END: R-PDD-GIT-001
## Purpose
Maintain a clean and traceable history of agent-led code changes.

## Rules
1. **Atomic Commits**: Agents SHOULD commit changes in small, logical units corresponding to sub-tasks.
2. **Metadata Traceability**: All commit messages MUST include the Swarm ID and the originating Linear Issue ID for full traceability.

# R-PDD-KG-001: Knowledge Graph Lifecycle Management
## Purpose
Optimize system memory and prevent context pollution in RAG-based lookups.

## Rules
1. **Retention Policy**: Nodes in the global knowledge graph older than 90 days with no recent access hits SHOULD be eligible for automated pruning.
2. **Background Execution**: Maintenance tasks (like pruning) MUST run as low-priority background processes to avoid impacting VGPU-heavy inference tasks.

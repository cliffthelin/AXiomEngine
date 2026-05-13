# R-PDD-SWARM-001: Agent Swarm Orchestration
## Purpose
Define the governance framework for multi-agent collaboration (Swarms).

## Rules
1. **Hierarchical Decomposition**: Complex goals MUST be broken down into atomic sub-tasks by a Planning Agent (e.g., Archon) before delegation.
2. **Infinite Recursion Protection**: Sub-agents MUST NOT spawn further sub-agents unless explicitly authorized in the task payload. Maximum depth is 3.
3. **Context Inheritance**: Every sub-task MUST inherit the root session's PDD context and citations.
4. **Result Aggregation**: The Swarm Coordinator is responsible for collecting and validating results from all sub-agents before declaring a goal complete.
5. **VGPU Quotas**: Swarms MUST request a total VGPU quota for the group. Individual agents within the swarm must share this quota or request slices from the `vgpu_manager`.

## Non-Goals
- Real-time consensus (use eventual consistency via Valkey).
- Peer-to-peer delegation without coordinator oversight.

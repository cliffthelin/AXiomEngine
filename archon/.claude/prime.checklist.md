# Active ARCHON-CLAUDE Checklist: prime.md

// RULE-START: G-ARCHON-CLAUDE-PRIME-001
// RULE-START: G-ARCHON-CLAUDE-PRIME-001
// RULE-END: G-ARCHON-CLAUDE-PRIME-001
- [ ] G-ARCHON-CLAUDE-PRIME-001: `packages/core/src/orchestrator/orchestratoragent.ts` — single entry point for all platforms (Section: 3. Identify Key Entry Points)
// RULE-END: G-ARCHON-CLAUDE-PRIME-001
// RULE-START: G-ARCHON-CLAUDE-PRIME-002
// RULE-START: G-ARCHON-CLAUDE-PRIME-002
// RULE-END: G-ARCHON-CLAUDE-PRIME-002
- [ ] G-ARCHON-CLAUDE-PRIME-002: `packages/core/src/handlers/commandhandler.ts` — slash command routing (no AI) (Section: 3. Identify Key Entry Points)
// RULE-END: G-ARCHON-CLAUDE-PRIME-002
// RULE-START: G-ARCHON-CLAUDE-PRIME-003
// RULE-START: G-ARCHON-CLAUDE-PRIME-003
// RULE-END: G-ARCHON-CLAUDE-PRIME-003
- [ ] G-ARCHON-CLAUDE-PRIME-003: `packages/server/src/index.ts` — server startup, adapter wiring, port allocation (Section: 3. Identify Key Entry Points)
// RULE-END: G-ARCHON-CLAUDE-PRIME-003
// RULE-START: G-ARCHON-CLAUDE-PRIME-004
// RULE-START: G-ARCHON-CLAUDE-PRIME-004
// RULE-END: G-ARCHON-CLAUDE-PRIME-004
- [ ] G-ARCHON-CLAUDE-PRIME-004: `packages/workflows/src/executor.ts` — sequential/parallel/loop/DAG workflow execution (Section: 3. Identify Key Entry Points)
// RULE-END: G-ARCHON-CLAUDE-PRIME-004
// RULE-START: G-ARCHON-CLAUDE-PRIME-005
// RULE-START: G-ARCHON-CLAUDE-PRIME-005
// RULE-END: G-ARCHON-CLAUDE-PRIME-005
- [ ] G-ARCHON-CLAUDE-PRIME-005: `packages/paths/src/index.ts` — path resolution + Pino logger (zero deps) (Section: 4. Understand Package Dependency Layers)
// RULE-END: G-ARCHON-CLAUDE-PRIME-005
// RULE-START: G-ARCHON-CLAUDE-PRIME-006
// RULE-START: G-ARCHON-CLAUDE-PRIME-006
// RULE-END: G-ARCHON-CLAUDE-PRIME-006
- [ ] G-ARCHON-CLAUDE-PRIME-006: `packages/git/src/index.ts` — git ops (depends only on @archon/paths) (Section: 4. Understand Package Dependency Layers)
// RULE-END: G-ARCHON-CLAUDE-PRIME-006
// RULE-START: G-ARCHON-CLAUDE-PRIME-007
// RULE-START: G-ARCHON-CLAUDE-PRIME-007
// RULE-END: G-ARCHON-CLAUDE-PRIME-007
- [ ] G-ARCHON-CLAUDE-PRIME-007: `packages/isolation/src/index.ts` — worktree isolation (depends on @archon/git + @archon/paths) (Section: 4. Understand Package Dependency Layers)
// RULE-END: G-ARCHON-CLAUDE-PRIME-007
// RULE-START: G-ARCHON-CLAUDE-PRIME-008
// RULE-START: G-ARCHON-CLAUDE-PRIME-008
// RULE-END: G-ARCHON-CLAUDE-PRIME-008
- [ ] G-ARCHON-CLAUDE-PRIME-008: `packages/workflows/src/index.ts` — workflow engine (depends on @archon/git + @archon/paths) (Section: 4. Understand Package Dependency Layers)
// RULE-END: G-ARCHON-CLAUDE-PRIME-008
// RULE-START: G-ARCHON-CLAUDE-PRIME-009
// RULE-START: G-ARCHON-CLAUDE-PRIME-009
// RULE-END: G-ARCHON-CLAUDE-PRIME-009
- [ ] G-ARCHON-CLAUDE-PRIME-009: Archon: Remote agentic coding platform (Slack, Telegram, GitHub, Discord, Web) (Section: Project Overview)
// RULE-END: G-ARCHON-CLAUDE-PRIME-009
// RULE-START: G-ARCHON-CLAUDE-PRIME-010
// RULE-START: G-ARCHON-CLAUDE-PRIME-010
// RULE-END: G-ARCHON-CLAUDE-PRIME-010
- [ ] G-ARCHON-CLAUDE-PRIME-010: Bun + TypeScript monorepo with 8 packages: paths, git, isolation, workflows, core, adapters, server, web (Section: Project Overview)
// RULE-END: G-ARCHON-CLAUDE-PRIME-010
// RULE-START: G-ARCHON-CLAUDE-PRIME-011
// RULE-START: G-ARCHON-CLAUDE-PRIME-011
// RULE-END: G-ARCHON-CLAUDE-PRIME-011
- [ ] G-ARCHON-CLAUDE-PRIME-011: SQLite (default, zerosetup) or PostgreSQL (optional via DATABASE_URL) (Section: Project Overview)
// RULE-END: G-ARCHON-CLAUDE-PRIME-011
// RULE-START: G-ARCHON-CLAUDE-PRIME-012
// RULE-START: G-ARCHON-CLAUDE-PRIME-012
// RULE-END: G-ARCHON-CLAUDE-PRIME-012
- [ ] G-ARCHON-CLAUDE-PRIME-012: Package dependency order and each package's responsibility (Section: Architecture)
// RULE-END: G-ARCHON-CLAUDE-PRIME-012
// RULE-START: G-ARCHON-CLAUDE-PRIME-013
// RULE-START: G-ARCHON-CLAUDE-PRIME-013
// RULE-END: G-ARCHON-CLAUDE-PRIME-013
- [ ] G-ARCHON-CLAUDE-PRIME-013: Key interfaces: `IPlatformAdapter`, `IAgentProvider`, `IDatabase`, `IWorkflowStore` (Section: Architecture)
// RULE-END: G-ARCHON-CLAUDE-PRIME-013
// RULE-START: G-ARCHON-CLAUDE-PRIME-014
// RULE-START: G-ARCHON-CLAUDE-PRIME-014
// RULE-END: G-ARCHON-CLAUDE-PRIME-014
- [ ] G-ARCHON-CLAUDE-PRIME-014: Message flow: platform adapter → orchestratoragent → command handler OR AI provider (Section: Architecture)
// RULE-END: G-ARCHON-CLAUDE-PRIME-014
// RULE-START: G-ARCHON-CLAUDE-PRIME-015
// RULE-START: G-ARCHON-CLAUDE-PRIME-015
// RULE-END: G-ARCHON-CLAUDE-PRIME-015
- [ ] G-ARCHON-CLAUDE-PRIME-015: Workflow execution: `discoverWorkflows` → router → `executeWorkflow` (steps / loop / DAG) (Section: Architecture)
// RULE-END: G-ARCHON-CLAUDE-PRIME-015
// RULE-START: G-ARCHON-CLAUDE-PRIME-016
// RULE-START: G-ARCHON-CLAUDE-PRIME-016
// RULE-END: G-ARCHON-CLAUDE-PRIME-016
- [ ] G-ARCHON-CLAUDE-PRIME-016: Active branch, recent changes, any uncommitted work (Section: Current State)
// RULE-END: G-ARCHON-CLAUDE-PRIME-016
// RULE-START: G-ARCHON-CLAUDE-PRIME-017
// RULE-START: G-ARCHON-CLAUDE-PRIME-017
// RULE-END: G-ARCHON-CLAUDE-PRIME-017
- [ ] G-ARCHON-CLAUDE-PRIME-017: Any observations relevant to next task (Section: Current State)
// RULE-END: G-ARCHON-CLAUDE-PRIME-017
// RULE-START: G-ARCHON-CLAUDE-PRIME-018
// RULE-START: G-ARCHON-CLAUDE-PRIME-018
// RULE-END: G-ARCHON-CLAUDE-PRIME-018
- [ ] G-ARCHON-CLAUDE-PRIME-018: Keep it scannable — bullets over prose. (Section: Current State)
// RULE-END: G-ARCHON-CLAUDE-PRIME-018

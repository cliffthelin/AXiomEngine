# Active ARCHON-RULECHECK Checklist: SKILL.md

- [ ] G-ARCHON-RULECHECK-SKILL-001: Do NOT scan the codebase yourself — that's the agent's job (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-002: Do NOT grep, read source files, or run linters — the agent handles all of that (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-003: Do NOT edit any files — you are the orchestrator, not the fixer (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-004: Do NOT try to resume or check on the agent while it's running — just wait (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-005: Do NOT do the agent's work if it fails or hits context limits — report the failure to the user and stop. NEVER pick up where the agent left off. You are not in a worktree and would be editing main directly. (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-006: Do NOT update project memory — the agent maintains its own memory at `.claude/agentmemory/rulecheckagent/`. Do not duplicate run results into your project memory. (Section: Rules for You)
- [ ] G-ARCHON-RULECHECK-SKILL-007: Trust the agent. It runs in an isolated worktree and will create a PR when done. (Section: Rules for You)

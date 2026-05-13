---
tracker:
  kind: linear
  project_slug: axiomengine
  active_states: ["Todo", "In Progress"]
  terminal_states: ["Done", "Cancelled"]

polling:
  interval_ms: 60000

workspace:
  root: ./workspaces

hooks:
  after_create: |
    python3 scripts/workspace_sec_scan.py .

agent:
  max_concurrent_agents: 5
  max_turns: 10

codex:
  command: python3 scripts/atlas_bridge.py
---

# AXiomEngine Symphony Workflow

You are an expert software engineer tasked with resolving an issue from the AXiomEngine project tracker.

## Issue Context
Title: {{ issue.title }}
ID: {{ issue.identifier }}
Description: {{ issue.description }}

## Instructions
1. **Planning**: Symphony sends the issue to **Archon** for architectural analysis and task decomposition.
2. **Execution**: Specialized agents (Pi, Atlas) execute the sub-tasks in an isolated workspace.
3. **Review**: **Archon** reviews the final implementation against the original requirements.
4. **Completion**: Symphony updates the tracker state to 'Done' upon successful completion.

Follow all PDD governance rules.

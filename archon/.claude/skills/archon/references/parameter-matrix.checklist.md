# Active ARCHON-REFERENCES Checklist: parameter-matrix.md

- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-001: Reading the matrix: (Section: Master Matrix: Parameters × Node Types)
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-002: yes — field works as expected on this node type. (Section: Master Matrix: Parameters × Node Types)
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-003: ignored — field is accepted by the parser but has no effect at runtime. Loader emits a warning (`<nodetype>_node_ai_fields_ignored`). (Section: Master Matrix: Parameters × Node Types)
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-004: hard error — workflow fails to load. Only `retry` on a loop node does this. (Section: Master Matrix: Parameters × Node Types)
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-005: id: analysis (Section: Inline `agents:` (Task-tool sub-agents))
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-006: Fields per agent: (Section: Inline `agents:` (Task-tool sub-agents))
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-007: Naming rule: lowercase kebabcase. No leading or trailing hyphens, no double hyphens, no digitsonly ids. (Section: Inline `agents:` (Task-tool sub-agents))
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-008: When to use `agents:` vs fanout at the workflow level: (Section: Inline `agents:` (Task-tool sub-agents))
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-009: Use `agents:` when the number of subtasks is dynamic or decided by the orchestrator node at runtime. (Section: Inline `agents:` (Task-tool sub-agents))
- [ ] G-ARCHON-REFERENCES-PARAMETER-MATRIX-010: Use workflowlevel fanout (parallel nodes with `depends_on: [setup]`) when the subtasks are known ahead of time and each needs its own artifact. (Section: Inline `agents:` (Task-tool sub-agents))

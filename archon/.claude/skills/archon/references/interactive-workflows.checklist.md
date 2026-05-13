# Active ARCHON-REFERENCES Checklist: interactive-workflows.md

- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-001: `archonpivloop` — PlanImplementValidate with iterative feedback (Section: Identifying Interactive Workflows)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-002: `archoninteractiveprd` — Guided PRD creation with approval gates (Section: Identifying Interactive Workflows)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-003: DON'T: (Section: Questions)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-004: It discovered that the json flag is partially implemented (Section: Questions)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-005: It's asking about the output format (Section: Questions)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-006: Read the latest output from the log (Section: 5. Repeat until workflow completes)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-007: Display it directly (Section: 5. Repeat until workflow completes)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-008: Wait for the user's response (Section: 5. Repeat until workflow completes)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-009: Resume with their response (Section: 5. Repeat until workflow completes)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-010: Workflow shows `running` for a long time: The AI is doing research/implementation. Be patient — check again in a few minutes. (Section: Troubleshooting)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-011: Log file not found: The log is at `~/.archon/workspaces/<owner>/<repo>/logs/<runid>.jsonl` (Section: Troubleshooting)
- [ ] G-ARCHON-REFERENCES-INTERACTIVE-WORKFLOWS-012: User wants to cancel: Run `archon workflow reject <runid>` to stop at an approval gate, or `archon workflow abandon <runid>` to mark the run cancelled without killing any subprocess. To actively terminate a stilllive subprocess, use the chat slash command `/workflow cancel <runid>` on the platform that started it — there is no `archon workflow cancel` CLI subcommand (Section: Troubleshooting)

# Active ARCHON-SAVE-TASK-LIST Checklist: SKILL.md

- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-001: hooks: (Section: General)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-002: type: prompt (Section: General)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-003: matcher: "Bash" (Section: General)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-004: type: command (Section: General)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-005: Session ID: ${CLAUDE_SESSION_ID} (Section: Session Context)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-006: Active task directories: !`ls 1t ~/.claude/tasks/ 2>/dev/null | head 5 || echo "none found"` (Section: Session Context)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-007: Current tasks in session: !`ls 1t ~/.claude/tasks/ 2>/dev/null | head 1 | xargs I{} ls ~/.claude/tasks/{} 2>/dev/null | head 10 || echo "no tasks"` (Section: Session Context)
- [ ] G-ARCHON-SAVE-TASK-LIST-SKILL-008: Important: Merge — don't overwrite existing settings. If `hooks` or `SessionStart` (Section: Instructions)

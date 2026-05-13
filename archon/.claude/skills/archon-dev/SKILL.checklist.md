# Active ARCHON-ARCHON-DEV Checklist: SKILL.md

- [ ] G-ARCHON-ARCHON-DEV-SKILL-001: Branch: !`git branch showcurrent 2>/dev/null || echo "not in git repo"` (Section: Current State)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-002: Artifacts: !`ls .claude/archon/ 2>/dev/null || echo "none yet"` (Section: Current State)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-003: Active plans: !`ls .claude/archon/plans/.plan.md 2>/dev/null | head 5 || echo "none"` (Section: Current State)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-004: Read `$ARGUMENTS` and determine which cookbook to load. (Section: Routing)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-005: If ambiguous: Ask the user which cookbook to use. (Section: Routing)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-006: After routing: Read the matched cookbook file and follow its instructions exactly. (Section: Routing)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-007: Package manager: Check for `bun.lockb` → bun, `pnpmlock.yaml` → pnpm, `yarn.lock` → yarn, else npm (Section: Project Detection)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-008: Validation command: Check `package.json` scripts for `validate`, `check`, or `verify` (Section: Project Detection)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-009: Test command: Check for `test` script in `package.json` (Section: Project Detection)
- [ ] G-ARCHON-ARCHON-DEV-SKILL-010: Conventions: Read CLAUDE.md for projectspecific rules (Section: Project Detection)

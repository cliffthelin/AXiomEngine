# Active ARCHON-REFERENCES Checklist: cli-commands.md

- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-001: Flag conflicts (errors): (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-002: `branch` + `noworktree` (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-003: `from` + `noworktree` (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-004: `resume` + `branch` (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-005: Default behavior (no flags): Autocreates a worktree with branch name `{workflowname}{timestamp}`. (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-006: Autoresume without `resume`: If a prior invocation of the same workflow at the same cwd failed, the next invocation automatically skips completed nodes. `resume` is only needed when you want to force resume a specific failed run or to reuse the worktree from that run. (Section: `archon workflow run <name> [message] [flags]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-007: Deletes old terminal workflow runs (`completed`/`failed`/`cancelled`) from the database for disk hygiene. Does NOT transition `running` rows — use `abandon`/`cancel` for those. (Section: `archon workflow cleanup [days]`)
- [ ] G-ARCHON-REFERENCES-CLI-COMMANDS-008: Flags: (Section: `archon isolation cleanup [days]`)

# Active ARCHON-MAINTAINER-STANDUP Checklist: README.md

// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-001
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-001
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-001
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-001: Set `gh_handle` to your GitHub login. (Section: Setup for a new maintainer)
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-001
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-002
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-002
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-002
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-002: Set `role` and `scope` to match your maintainer focus (`main_maintainer` / `everything` for full coverage; narrower for submaintainers). (Section: Setup for a new maintainer)
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-002
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-003
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-003
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-003
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-003: Optionally fill in Currently focused on — the synthesizer weights items toward what you list there. (Section: Setup for a new maintainer)
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-003
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-004
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-004
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-004
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-004: `maintainerstandupgitstatus.ts` — fetches `origin/dev`, fastforwards if safe, captures new commits + diff stat since the last recorded SHA. (Section: How it works (engine view))
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-004
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-005
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-005
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-005
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-005: `maintainerstandupghdata.ts` — pulls open PRs (full metadata), reviewrequested PRs, authoredbyme PRs, assigned issues, recentlyfiled unlabeled issues, and recentlyclosed PRs/issues since the last run. (Section: How it works (engine view))
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-005
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-006
// RULE-START: G-ARCHON-MAINTAINER-STANDUP-README-006
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-006
- [ ] G-ARCHON-MAINTAINER-STANDUP-README-006: `maintainerstandupreadcontext.ts` — reads `direction.md`, `profile.md`, `state.json`, and the last 3 briefs. (Section: How it works (engine view))
// RULE-END: G-ARCHON-MAINTAINER-STANDUP-README-006

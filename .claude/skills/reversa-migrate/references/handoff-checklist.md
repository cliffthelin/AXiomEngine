```markdown
# `handoff.md` Checklist

Before closing the pipeline, the orchestrator validates that `handoff.md` meets all the listed criteria.

## Mandatory Checklist

- [ ] `paradigm_decision.md` appears as the **first item** in both the "Required Reading" section and the "Recommended Reading Order" section.
- [ ] `topology_decision.md` appears as the **second item** in the "Required Reading" section.
- [ ] `screen_modernization_decision.md` appears as the **third item** when a UI exists; in legacy systems without a UI (Screen Translator skipped), the entry is omitted with an explicit note: "Screen Translator skipped, legacy system without UI".
- [ ] The list of artifacts produced is complete and accurately reflects the contents of `_reversa_sdd/migration/` and `_reversa_sdd/screens/`.
- [ ] Pending deviations in `screen_deviation_log.md` are identified as blockers; approved deviations are reflected in `parity_specs.md § Exceptions`.
- [ ] Items REFERENCED IN THE CODE from `ambiguity_log.md` appear in a dedicated section of `handoff.md`.
- [ ] Blockers are listed, or the statement "no blockers, proceed" is present.
- [ ] The next steps for the coding agent are specific and actionable (not generic).
- [ ] In `--auto` mode, auto-decided items are listed explicitly.
- [ ] The style is consistent with the installed engine (adapted format, e.g., compatible front-matter).

## Minimum Structure

1. Required reading banner from `paradigm_decision.md`, `topology_decision.md`, and (if a UI exists) `screen_modernization_decision.md`.
2. Recommended reading order.
3. Artifact list.
4. Blockers.
5. Next steps for the coding agent.
6. Auto-decided items (only if `--auto`).
7. Final notes.

## Strong Signaling to the Coding Agent

The first sentence of `handoff.md` should convey immediate clarity. Suggested format:

> "New system to be built with paradigm <X>, topology <Y>, and screens in mode <Z>. Before writing any code, read `paradigm_decision.md`, `topology_decision.md`, and `screen_modernization_decision.md`."

In legacy systems without a UI (Screen Translator skipped), replace the screens section with: "screens: none (system without UI)."
```
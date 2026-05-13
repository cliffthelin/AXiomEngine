### SOURCE:
# `handoff.md` Checklist

Before closing the pipeline, the orchestrator validates that `handoff.md` meets all the requirements.

## Mandatory Checklist

- [ ] `paradigm_decision.md` appears as the **first item** in both the "Required Reading" and "Recommended Reading Order" sections.
- [ ] `topology_decision.md` appears as the **second item** in the "Required Reading" section.
- [ ] `screen_modernization_decision.md` appears as the **third item** when a UI exists; in legacy applications without a UI (Screen Translator skipped), the entry is omitted with an explicit note: "Screen Translator skipped, legacy application without UI."
- [ ] The list of produced artifacts is complete and reflects the actual contents of `_reversa_sdd/migration/` and `_reversa_sdd/screens/`.
- [ ] Pending deviations in `screen_deviation_log.md` are listed as blockers; approved deviations are reflected in `parity_specs.md § Exceptions`.
- [ ] Items **REFERENCED IN THE CODE** from `ambiguity_log.md` appear in a dedicated section of `handoff.md`.
- [ ] Blockers are listed, or the line "no blockers, proceed" is present.
- [ ] Next steps for the coding agent are specific and actionable (not generic).
- [ ] In `--auto` mode: auto-decided items are listed explicitly.
- [ ] Consistent style with the installed engine (adapted format, e.g., compatible front-matter).

## Minimum Structure

1. Required Reading banner of `paradigm_decision.md`, `topology_decision.md`, and (if a UI exists) `screen_modernization_decision.md`.
2. Recommended Reading Order.
3. Artifact List.
4. Blockers.
5. Next steps for the coding agent.
6. Auto-decided items (only if `--auto`).
7. Final notes.

## Strong Signal to the Coding Agent

The first sentence of `handoff.md` should convey immediate clarity. Suggested pattern:

> "New system to be built in paradigm <X>, topology <Y>, screens in mode <Z>. Before any lines of code are written, read `paradigm_decision.md`, `topology_decision.md`, and `screen_modernization_decision.md`."

In legacy applications without a UI (Screen Translator skipped), replace the screens section with: "screens: none (application without UI)."

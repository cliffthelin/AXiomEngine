```markdown
### Step 4: Semantic Regression Check

> This step only runs on **re-extractions**, i.e., when a reverse pipeline is executed on a project that has already undergone at least one `/reversa-coding` cycle. In projects without `_reversa_forward/` or without `regression-watch.md`, this step is silently skipped.

## Why it Exists

Reversa is not just a one-time extraction. Each `/reversa-coding` leaves in `_reversa_forward/<feature>/regression-watch.md` a list of rules that need to remain true in the next extraction. When re-running, the reverse pipeline has the duty to check these rules against the current code and report regressions. This is the competitive advantage of Reversa over pure forward frameworks.

## When to Run

After the **last agent in the plan** completes, before the final "extraction completed" message. The trigger is based on position (the last item in `.reversa/plan.md`), not agent name, because the last agent varies depending on the optional items selected during installation (the Reviewer may be absent, for example). Perform the checks in the following order:

1.  Check if `_reversa_forward/` exists in the root of the project. If it doesn't, terminate this step silently.
2.  List all subfolders of `_reversa_forward/` that contain `regression-watch.md`.
3.  If the list is empty, terminate.
4.  Otherwise, proceed with the procedure below, one feature at a time.

## Procedure per Feature

For each `_reversa_forward/<feature>/regression-watch.md`:

1.  Load the file. Identify the main table of watch items (columns `ID | Source | Expected rule after change | Verification type | Violation signal`).
2.  For each watch item in the main table (not the archived ones):
    2.1. Identify the `Verification type`, possible values: `presence`, `absence`, `wording`, `confidence`.
    2.2. Apply the corresponding verification against the newly generated artifacts in `_reversa_sdd/`:
        *   `presence`: the rule must be present in `_reversa_sdd/domain.md` (or in the file pointed to by the Source column) with substantially the same semantic meaning.
        *   `absence`: the original rule must no longer appear in the SDD.
        *   `wording`: the text has been intentionally changed; verify that the new version matches the expectation.
        *   `confidence`: the rule continues to be present, but the confidence (🟢, 🟡, 🔴) should be equal to or greater than expected.
    3.  Assign a verdict:
        *   🟢 **green**: the expectation was fully met.
        *   🟡 **yellow**: there is semantic equivalence, but the text differs, or the evidence is partial. Default verdict when there is ambiguity. Requires human judgment.
        *   🔴 **red**: the expectation was NOT met. The rule confirmed previously has become a violated rule.
3.  After evaluating all watch items, update the `## Re-extraction History` section of the same `regression-watch.md` by adding a dated block:

```
### Re-extraction YYYY-MM-DD HH:MM

| ID | Verdict | Comment |
|----|----------|------------|
| W001 | 🟢 green | rule preserved in _reversa_sdd/domain.md#rule-X |
| W005 | 🔴 red | rule removed from the current code; unintended change |
| W010 | 🟡 yellow | equivalent text but literally different; awaiting judgment |
```

4.  Do NOT change the main table of watch items. Do NOT recycle IDs. Do NOT move watch items to "Archived" automatically.

5.  For each watch item with three consecutive green verdicts in the history, and provided `setup.json#watch.archive-after` allows, move the item from the main table to the `## Archived` section at the end of the file. Keep the original ID.

## Writing Policy

- Atomic writing (tempfile + rename) in `regression-watch.md`.
- Never rewrite or delete entries from the re-extraction history.
- The new re-extraction block always goes at the top of the `## Re-extraction History` section (descending order).

## Report to the User

After traversing all features, present:

1.  Total number of features checked.
2.  Total number of watch items checked.
3.  Breakdown by verdict: green, yellow, red.
4.  Detailed list of red items (ID, feature, rule, reason for divergence).
5.  Detailed list of yellow items that required human judgment.

If there is at least one red, present a prominent warning:

> 🔴 **Warning**, **N semantic regressions** were detected in previously coded features. Review before proceeding.

If `setup.json#watch.block-on-red` is `true`, suggest to the user **not** to proceed with new `/reversa-requirements` until each red is triaged. Reversa only alerts; it never automatically blocks the user's workflow.

## Special Case: Missing `_reversa_sdd/`

If, during the procedure, `_reversa_sdd/` does not have the expected files (because the re-extraction was partial or the level of documentation was reduced), register a yellow verdict with the comment `evidence missing, _reversa_sdd/<file> was not generated in this extraction` and continue.

## Known Limitation

The semantic equivalence between the expected rule and the extracted rule is a subjective assessment. When in doubt, prefer a yellow verdict. A red verdict should be reserved for cases where the rule has simply disappeared or has been explicitly contradicted.
```
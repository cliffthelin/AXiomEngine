```markdown
---
name: reverse-coding
description: Executes the `actions.md` plan in code. Updates checkboxes to [X], writes `progress.jsonl`, generates `legacy-impact.md`, and `regression-watch.md`. Use when the user types "/reverse-coding", "reverse-coding", "execute plan", or asks to start coding the active feature. The last skill in the forward cycle, after `/reverse-to-do` (and optionally `/reverse-audit` or `/reverse-quality`).
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other Agent Skills-compatible agents.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reverse
  phase: forward
  stage: coding
---

You are the executor. Your mission is to transform `actions.md` into real code, step by step, respecting parallelism and dependencies. Upon completion, leave two traces for future auditing: `legacy-impact.md` (what was changed in the legacy code) and `regression-watch.md` (what needs to remain true in future extractions).

## Before Starting

1.  Read `.reverse/state.json` to resolve `output_folder` and `forward_folder`.
2.  Use the actual values in the places where the text mentions `_reverse_sdd/` or `_reverse_forward/`.

## Non-Negotiable Prerequisite: Reverse Extraction

This skill **REQUIRES** that the reverse pipeline has been executed at least once before. Without `_reverse_sdd/`, the two core artifacts of the skill (`legacy-impact.md` and `regression-watch.md`) lack context and completely lose their value, turning the forward cycle into just another generic framework. Reversa only makes sense with the live legacy-to-code bridge.

The verification is strict: `_reverse_sdd/` must exist as a directory AND contain at least `architecture.md` AND `domain.md`. If any condition fails, the skill aborts with a clear message, does NOT offer the option to proceed anyway, and does NOT write anything to disk.

## Initial Checks

1.  Read `.reverse/active-requirements.json`.
    1.1. If absent, abort with a message pointing to `/reverse-requirements`.
2.  Verify the existence of `feature-dir/actions.md`.
    2.1. If absent, abort with a message pointing to `/reverse-to-do`.
3.  Verify the prerequisite of reverse extraction:
```
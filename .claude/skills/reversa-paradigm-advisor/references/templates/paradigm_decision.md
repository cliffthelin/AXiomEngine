```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: paradigm_decision
producedBy: paradigm_advisor
hash: "sha256:<hash of the body below the front-matter>"
---

# Paradigm Decision

> A conscious decision on how to handle the shift (or lack thereof) in paradigm between the legacy system and the target stack.
> This artifact is required reading for any subsequent agent and for the coding agent.

## Legacy Paradigm Detected
- **Main Paradigm**: <procedural | classic OO | OO with DI | functional | event-driven | actor model | dataflow | hybrid: ...>
- **Confidence**: 🟢 CONFIRMED | 🟡 INFERRED | 🔴 GAP | ⚠️ AMBIGUOUS
- **Evidence**:
  - <evidence 1, referencing an artifact from `_reversa_sdd/`>
  - <evidence 2>
- **Observed Variations** (if hybrid):
  - <component A: paradigm X, evidence>
  - <component B: paradigm Y, evidence>

## Declared Target Stack
- Language: <from migration_brief.md>
- Framework: <from migration_brief.md>
- Infrastructure: <from migration_brief.md>

## Inferred Natural Paradigm
- **Paradigm**: <inferred via paradigm_catalog>
- **Justification**: <why this stack has this natural paradigm>
- **Viable Alternatives**: <e.g., OO with DI is also viable in Node, at cost X>

## Identified Gap
- **Severity**: high | medium | low | none
- **Concrete Implications** (not abstract; with an example from the legacy system itself):
  - <implication 1, citing a rule/flow from the affected legacy system>
  - <implication 2>
  - <implication 3>
  - <implication 4>

## Options Presented to the User
1. **Adopt the natural paradigm of the stack** (transformational)
   - Consequences: <list>
2. **Enforce a paradigm similar to the legacy system** (conservative)
   - Consequences: <list>
3. **Hybrid** (balanced)
   - Consequences: <list>

## User Decision
- **Choice**: <1 | 2 | 3>
- **User Justification**: <free text>
- **Decided On**: <ISO-8601>

## Derived Appetite
- `derived_appetite`: conservative | balanced | transformational

## Pending Implications for Subsequent Agents
| Agent | Implication | How to honor |
|---|---|---|
| Curator | <implication> | <expected action> |
| Strategist | <implication> | <expected action> |
| Designer | <implication> | <expected action> |
| Inspector | <implication> | <expected action> |

## Notes
<Any additional point that the coding agent needs to know about the target paradigm.>
```
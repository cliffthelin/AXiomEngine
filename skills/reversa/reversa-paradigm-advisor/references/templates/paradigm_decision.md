```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: paradigm_decision
producedBy: paradigm_advisor
hash: "sha256:<hash do corpo abaixo do front-matter>"
---

# Paradigm Decision

> A conscious decision about how to handle the shift (or lack thereof) in paradigm between the legacy system and the target stack.
> This artifact is essential reading for any subsequent agent and the coding agent.

## Detected Legacy Paradigm
- **Primary Paradigm**: <procedural | classic OO | OO with DI | functional | event-driven | actor model | dataflow | hybrid: ...>
- **Confidence**: 🟢 CONFIRMED | 🟡 INFERRED | 🔴 GAP | ⚠️ AMBIGUOUS
- **Evidence**:
  - <evidence 1, with reference to the artifact in `_reversa_sdd/`>
  - <evidence 2>
- **Observed Variations** (if hybrid):
  - <Component A: Paradigm X, Evidence>
  - <Component B: Paradigm Y, Evidence>

## Declared Target Stack
- Language: <from migration_brief.md>
- Framework: <from migration_brief.md>
- Infrastructure: <from migration_brief.md>

## Inferred Natural Paradigm
- **Paradigm**: <inferred via paradigm_catalog>
- **Justification**: <why this stack has this natural paradigm>
- **Viable Alternatives**: <e.g., OO with DI is also viable in Node, with cost X>

## Identified Gap
- **Severity**: high | medium | low | none
- **Concrete Implications** (not in abstract; with an example from the legacy system):
  - <implication 1, citing a rule/flow from the affected legacy system>
  - <implication 2>
  - <implication 3>
  - <implication 4>

## Options Presented to the User
1. **Adopt the natural paradigm of the stack** (transformational)
   - Consequences: <list>
2. **Force a paradigm similar to the legacy system** (conservative)
   - Consequences: <list>
3. **Hybrid** (balanced)
   - Consequences: <list>

## User Decision
- **Choice**: <1 | 2 | 3>
- **User Justification**: <free text>
- **Decided on**: <ISO-8601>

## Derived Appetite
- `derived_appetite`: conservative | balanced | transformational

## Pending Implications for Subsequent Agents
| Agent | Implication | How to address |
|---|---|---|
| Curator | <implication> | <expected action> |
| Strategist | <implication> | <expected action> |
| Designer | <implication> | <expected action> |
| Inspector | <implication> | <expected action> |

## Notes
<Any additional points that the coding agent needs to know about the target paradigm.>
```
```
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: topology_decision
producedBy: designer
hash: "sha256:<hash of the body below the front-matter>"
---

# Topology Decision

> A conscious decision about how to organize the new system: preserve the legacy topology, adopt a modern topology, or apply a hybrid approach.
> This artifact is required reading for both the Designer (to decompose bounded contexts) and the coding agent (to create the folder tree).

## Detected Legacy Topology
- **Organizational pattern**: <package-by-layer | package-by-feature | feature-sliced | modules-by-domain | DDD with bounded contexts | monorepo | monolithic with unclear boundaries | hybrid: ...>
- **Confidence**: 🟢 CONFIRMED | 🟡 INFERRED | 🔴 GAP | ⚠️ AMBIGUOUS
- **Evidence**:
  - <evidence 1, with reference to an artifact in the `_reversa_sdd/` directory (architecture.md, inventory.md, dependencies.md)>
  - <evidence 2>
- **Summary of the legacy tree**:
  ```
  <short tree with main folders/modules>
  ```

## Structural Diagnosis
- **Coupling**: <high | medium | low, with evidence>
- **Module Cohesion**: <high | medium | low, with evidence>
- **Orphaned/Dead Modules**: <list, or "none">
- **Redundant Layers**: <list, or "none">
- **Boundary Violations**: <list, or "none">
- **Mixing of Paradigms/Styles**: <description, or "homogeneous">
- **Overall Assessment**: <healthy | problematic | partially problematic>

## Proposed Modern Topology
- **Pattern**: <hexagonal | vertical slices | feature-sliced | DDD with bounded contexts | package-by-feature | modularization by capability | monorepo with pnpm/turborepo | ...>
- **Justification**: <why this pattern fits the target stack, the domain, the team size, and the chosen migration strategy>
- **Expected Concrete Gains**:
  - <gain 1: e.g., isolated testability per feature>
  - <gain 2: e.g., independent deployment per bounded context>
  - <gain 3: e.g., faster onboarding>
- **Cost/Risk**:
  - <cost 1: e.g., team learning curve>
  - <cost 2: e.g., reorganization effort>
- **Sketch of the Proposed Tree**:
  ```
  <short tree with folders/modules in the modern pattern>
  ```

## Options Presented to the User
1. **Preserve legacy topology** (conservative)
   - Consequences: maintains the current team's mental map; perpetuates any existing structural debt; reduces migration risk.
2. **Adopt proposed modern topology** (transformational)
   - Consequences: breaks with structural debt; requires learning; maximizes gains from the target stack.
3. **Hybrid** (balanced)
   - Consequences: <describe which boundaries preserve the legacy and which adopt the modern approach, with justification for each boundary>

## User Decision
- **Choice**: <1 | 2 | 3>
- **User Justification**: <free text>
- **Decided on**: <ISO-8601>

## Legacy → New Mapping
| Legacy Module/Folder | New Bounded Context | Type | Notes |
|---|---|---|---|
| <legacy A> | <new X> | preserved | <notes> |
| <legacy B + C> | <new Y> | merged | <justification> |
| <legacy D> | <new Y1, Y2> | split | <justification> |
| (empty) | <new Z> | new | <justification> |
| <legacy E> | (discarded) | removed | see `discard_log.md` |

## Pending Implications for the Designer's Next Steps
| Designer Stage | Implication | How to Address |
|---|---|---|
| Bounded contexts | <implication> | <expected action> |
| target_architecture | <implication> | <expected action> |
| target_domain_model | <implication> | <expected action> |
| target_data_model | <implication> | <expected action> |

## Notes
<Any additional point that the coding agent needs to know in order to create the folder樹 and respect the chosen topology.>
```
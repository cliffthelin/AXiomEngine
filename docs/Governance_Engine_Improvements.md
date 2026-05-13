# Governance Engine — Critical Review & Improvement Recommendations

> This is an honest assessment of gaps, weaknesses, and unconsidered areas
> in the 13-layer architecture as currently implemented.

---

## 1. Structural Weaknesses in Current Implementation

### 1A. DataConcept Matching Is Too Shallow (4.2% coverage)

**Problem**: DataConcepts currently match files by simple substring alias matching against file paths. This produces:
- Only 76 of 1,830 files matched (4.2%)
- False negatives: a file like `dag-executor.ts` has no alias that would match any concept
- False positives possible: a concept alias of "session" would match both `agent_session.py` and `test-sessions.ts`

**Recommendation**: DataConcepts should not be matched by filename alone. They need a **mapping table** — an explicit, human-authored binding between concepts and files/modules. This is the "hard work" layer that cannot be automated.

```yaml
# Proposed: explicit bindings
DataConceptBinding:
  concept_id: DC-GPU-THERMAL-LIMIT
  bound_files:
    - scripts/gpu_thermal_optimizer.py
    - scripts/gpu_thermal_optimizer.py  # implementation
  bound_rules:
    - R-HW-GPU-001
  bound_decisions:
    - DEC-P40-POWER-LIMIT-150W
```

Without explicit bindings, the alignment scores are **inflated or deflated by regex quality**, not governance quality.

---

### 1B. MDG Has No REQUIRES Edges (0 found)

**Problem**: The MDG builder creates IMPLEMENTED_BY and INTERPRETS edges, but **zero REQUIRES edges**. This means the core dependency chain from the Layers Conversation — `Authority → Concept → Rule → Validation → Code` — is not actually materialized.

**Root Cause**: The rule-to-concept matching uses scope strings (e.g., "hw", "core") compared against aliases, which rarely match.

**Recommendation**: Rules should explicitly declare which DataConcept they govern:
```json
{"rule_id": "R-HW-GPU-001", "governs": "DC-GPU-THERMAL-LIMIT"}
```

This creates the backbone chain the MDG needs.

---

### 1C. No Conflict Detection Between Layers

**Problem**: The Layers Conversation is explicit: *"Your strength is the tension between layers, not their agreement."* But the current engine only measures **coverage** (does a layer exist?), not **conflict** (do layers disagree?).

**Example**: Reversa could find that code allows 200W power draw, while Decision DEC-P40-POWER-LIMIT-150W says 150W max. Currently, both would show as "covered" with no conflict flagged.

**Recommendation**: Add a **Conflict Detector** that cross-references:
- L2 (Reversa observed behavior) vs. L3 (PDD declared rules)
- L6 (Decisions) vs. L1 (Code reality)
- L3 (Rules) vs. L4 (Authority — is the rule actually authorized?)

Conflicts are the highest-value governance signals. They should be first-class outputs, not invisible.

---

## 2. Missing Capabilities

### 2A. No Temporal Replay

**Problem**: The Layers Conversation dedicates significant attention to temporal edges — the ability to ask "Was this correct on October 1, 2024?" Currently, L12 (Temporal) is at 0% and no tooling exists to query historical state.

**What's Needed**:
- Snapshot the Intent Index on every significant change (git tag, governance decision, rule update)
- Store snapshots with timestamps
- A query tool: `python3 scripts/temporal_query.py --date 2025-10-01 DC-GPU-THERMAL-LIMIT`

Without this, the engine can only answer "is this correct NOW?" — which is insufficient for audit.

---

### 2B. No Automated Trigger Detection

**Problem**: The Layers Conversation identifies that the biggest systemic risk is **trigger weakness** — updates are human-driven, not event-driven. The ProcessRecords define trigger events (CodeDeployed, LawChanged, etc.), but nothing actually watches for these events.

**What's Needed**:
- Git hooks that trigger `intent_index_builder.py` on push
- A file watcher on `data/decisions.json` and `data/data_concepts.json` that triggers MDG rebuild
- Optional: a lightweight daemon that polls for governance artifact changes

---

### 2C. No Validation Layer Population (L11)

**Problem**: L11 (Validation/Enforcement) is at 0%. The engine doesn't distinguish between rules that are:
- **Fatal** — must block execution
- **Warning** — should flag but not block
- **Informational** — nice to know

Without this, the pre-flight check treats all constraints equally. In practice, some rules are hard stops and others are advisory.

---

### 2D. No Obligation Actor Modeling (L7)

**Problem**: L7 (Obligations) is at 0%. The engine doesn't know WHO is responsible for what. In the AXiomEngine context:
- Which rules does the **AI agent** enforce?
- Which rules does the **human operator** enforce?
- Which rules does the **CI/CD system** enforce?

Without actor scoping, every rule appears to apply to everyone.

---

## 3. Conceptual Gaps Not Yet Addressed

### 3A. The Engine Cannot Govern Itself

**Problem**: The governance engine's own scripts (`intent_index_builder.py`, `mdg_builder.py`, etc.) are not governed by the governance engine. There are no DataConcepts, Rules, or Decisions about how the engine itself should behave.

**Risk**: The engine could drift without detection.

**Recommendation**: Create a `DC-GOVERNANCE-ENGINE` DataConcept and rules governing:
- Schema must not change without a Decision record
- DataConcept IDs must be stable and never reused
- MDG must be rebuilt after any upstream change

---

### 3B. No "Ungoverned by Design" Classification

**Problem**: Currently, a file with low alignment is classified as 🔴 UNGOVERNED, which implies it *should* be governed but isn't. But some files are intentionally outside governance scope:
- Generated files (`*.generated.ts`, `package-lock.json`)
- Third-party vendored code
- Test fixtures and mock data

**Recommendation**: Add an exclusion list or a "Not Applicable" classification so these files don't pollute the drift report.

---

### 3C. No Cross-Application Portability Story

**Problem**: The user clarified that AXiomEngine is the sandbox — the engine should work on any application. But currently:
- `PROJECT_ROOT` is hardcoded to `/mnt/UBUNTU_8TB/Projects/axiomengine`
- The governance report parser assumes a specific markdown table format
- DataConcepts, Decisions, and Rules are stored in AXiomEngine-specific paths

**Recommendation**: Refactor to accept `--project-root` as a CLI argument. All paths should be relative to this root. The engine becomes a tool you point at any repository.

---

### 3D. No Derivation Chain Tracking (L5)

**Problem**: L5 (Derived Logic) is at 0%. In the Layers Conversation, this was identified as critical — computed values like ADM (Average Daily Membership) depend on other DataConcepts. If a dependency changes, derived values may silently break.

**AXiomEngine Example**: The alignment score itself is a derived value. It depends on all 13 layers. If the weight formula changes, every historical score becomes non-comparable — but nothing tracks this derivation chain.

---

## 4. Process & Operational Gaps

### 4A. Decision Capture Has No Workflow

**Problem**: Decisions are the hardest layer to populate and the most dangerous to skip. Currently, someone has to manually edit `decisions.json`. There is no:
- Template or wizard to guide decision capture
- Validation that required fields are present
- Notification when a decision is about to expire (end_date approaching)

**Recommendation**: A simple CLI tool:
```bash
python3 scripts/capture_decision.py \
  --type Override \
  --concept DC-GPU-THERMAL-LIMIT \
  --rationale "Thermal crashes at default power" \
  --authority "Infrastructure Lead"
```

---

### 4B. No Governance Health Dashboard

**Problem**: The drift report is a static markdown file. For ongoing monitoring, a live dashboard showing:
- Layer coverage trends over time
- Recently added/expired decisions
- Files with degrading alignment scores
- MDG edge staleness

would make governance operationally sustainable rather than a periodic exercise.

---

### 4C. No "Governance Debt" Metric

**Problem**: Like technical debt, governance has a cost of deferral. Currently, there's no way to quantify "how much would it cost to fully govern this codebase?" 

**Recommendation**: A governance debt score per file:
```
Debt = (code_chars × (1.0 - alignment_score)) × complexity_weight
```

Summed across the codebase, this gives a single number executives can track.

---

## 5. Priority Ranking

If I had to pick the **top 5 most impactful improvements**:

| # | Improvement | Why |
|:---|:---|:---|
| 1 | **Explicit DataConcept→File bindings** | Without this, alignment scores are noise |
| 2 | **Conflict detection between layers** | Conflicts are the highest-value signals |
| 3 | **CLI portability (`--project-root`)** | Required for the engine to work on other apps |
| 4 | **"Not Applicable" file exclusions** | Removes false noise from drift reports |
| 5 | **Decision capture CLI tool** | Lowers the barrier to populating the hardest layer |

---

*This review is based on the current implementation state. Many of these gaps are natural consequences of building a v1 proof-of-concept — the architecture from the Layers Conversation is sound, the implementation just needs deepening.*

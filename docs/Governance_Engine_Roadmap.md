# Governance Engine — Research Areas & Direct Steps

> Organized by the 5 critical gaps identified in the improvement review,
> followed by research areas for deeper capabilities.

---

## Part 1: Direct Steps (Actionable Now)

### Fix 1: Explicit DataConcept Bindings

**Problem**: Alias-based substring matching yields 4.2% coverage.

**Direct Steps**:

1. **Create a bindings file** (`data/concept_bindings.json`) with explicit concept→file mappings:
   ```json
   {
     "DC-GPU-THERMAL-LIMIT": {
       "files": ["scripts/gpu_thermal_optimizer.py"],
       "rules": ["R-HW-GPU-001"],
       "decisions": ["DEC-P40-POWER-LIMIT-150W"]
     }
   }
   ```

2. **Modify `intent_index_builder.py`** to read bindings as the primary L8 source, falling back to alias matching only for unbound concepts.

3. **Seed the bindings** by running a one-time pass: for each DataConcept, query the Knowledge Graph and Reversa SDD for related files, then have a human confirm the mappings.

4. **Validation rule**: Every DataConcept MUST have at least one explicit file binding. Unbounded concepts are flagged in the drift report.

**Effort**: ~2 hours for the code change, ~1 hour per 10 concepts for manual binding.

---

### Fix 2: Conflict Detection Engine

**Problem**: Layers are checked for presence, not agreement.

**Direct Steps**:

1. **Create `scripts/conflict_detector.py`** that cross-references layer pairs:

   | Comparison | What It Catches |
   |:---|:---|
   | L2 (Reversa) vs L3 (Rules) | Code does something that violates a declared rule |
   | L6 (Decision) vs L1 (Code) | Decision says X, code still does Y |
   | L3 (Rules) vs L4 (Authority) | Rule exists but has no authorization backing |
   | L6 (Decision) vs L12 (Temporal) | Decision has expired but code still follows it |

2. **Conflict schema**: Each detected conflict gets a severity and a recommended action:
   ```yaml
   Conflict:
     conflict_id: CONF-001
     type: BehaviorVsRule
     layer_a: {layer: L2, finding: "Code allows 200W"}
     layer_b: {layer: L6, decision: "DEC-P40-POWER-LIMIT-150W says 150W"}
     severity: Critical
     recommended_action: "Align code to decision or create new override decision"
   ```

3. **Integrate into drift report** as a dedicated "Active Conflicts" section.

**Effort**: ~3 hours for the detector, ongoing value as layers are populated.

---

### Fix 3: CLI Portability

**Problem**: Hardcoded paths prevent use on other applications.

**Direct Steps**:

1. **Add `--project-root` argument** to all scripts:
   ```bash
   python3 scripts/intent_index_builder.py --project-root /path/to/other/app
   ```

2. **Replace all `PROJECT_ROOT = Path("/mnt/...")` constants** with:
   ```python
   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("--project-root", default=".", type=Path)
   args = parser.parse_args()
   PROJECT_ROOT = args.project_root.resolve()
   ```

3. **Standardize the expected directory layout** for any governed project:
   ```
   <project-root>/
   ├── data/
   │   ├── governance_schema.yaml
   │   ├── data_concepts.json
   │   ├── decisions.json
   │   ├── concept_bindings.json
   │   └── process_records/
   ├── pdd/
   │   └── load_rules.py
   ├── INTENT_INDEX.json       (generated)
   ├── MDG.json                (generated)
   └── GOVERNANCE_DRIFT_REPORT.md (generated)
   ```

4. **Create an `init` command** that scaffolds this structure for a new project:
   ```bash
   python3 scripts/governance_init.py --project-root /path/to/app
   ```

**Effort**: ~2 hours for refactoring, ~1 hour for the init scaffolder.

---

### Fix 4: "Not Applicable" Exclusions

**Problem**: Generated files, lock files, and vendored code pollute drift reports.

**Direct Steps**:

1. **Create `data/exclusions.json`**:
   ```json
   {
     "patterns": [
       "*.generated.ts",
       "package-lock.json",
       "CHANGELOG.md",
       "CHANGELOG.checklist.md",
       "*.test.ts",
       "*.test.py"
     ],
     "reason": "Generated, vendored, or test files — governance not applicable"
   }
   ```

2. **Add exclusion support to `intent_index_builder.py`**: Excluded files get a verdict of `⚪ N/A` and are removed from alignment score calculations.

3. **Impact**: This alone would dramatically improve the signal-to-noise ratio. The current top drift risks are `CHANGELOG.md`, `package-lock.json`, and `*.generated.ts` — all false positives.

**Effort**: ~30 minutes.

---

### Fix 5: Decision Capture CLI

**Problem**: Editing raw JSON is high friction for the most critical layer.

**Direct Steps**:

1. **Create `scripts/capture_decision.py`**:
   ```bash
   python3 scripts/capture_decision.py \
     --type Override \
     --concept DC-GPU-THERMAL-LIMIT \
     --rationale "Thermal crashes at default power limits" \
     --authority "Infrastructure Lead" \
     --evidence "gpu-manager.sh commit 2026-05-11" \
     --enforcement Strict \
     --expectation "Daemon MUST enforce 150W-220W stepping"
   ```

2. The script:
   - Auto-generates a stable `decision_id` (DEC-{concept}-{seq})
   - Sets `start_date` to today
   - Validates required fields
   - Appends to `data/decisions.json`
   - Triggers MDG rebuild

**Effort**: ~1 hour.

---

## Part 2: Research Areas (Require Investigation)

### Research 1: Automated DataConcept Discovery

**Question**: Can we auto-discover DataConcepts from code instead of defining them manually?

**Approaches to investigate**:
- **AST analysis**: Parse Python/TypeScript ASTs and extract class names, module docstrings, and function clusters as candidate concepts
- **LLM-assisted extraction**: Feed file contents to a local model (Qwen/Gemma on the P40) with the prompt: "What are the 3 core domain concepts in this file?"
- **Reversa integration**: The Reversa Architect agent already extracts "modules" — these could seed DataConcepts

**Risk**: Auto-discovered concepts may not match human mental models. Always requires human review.

**Research path**: Run a pilot on 10 files from `scripts/`, compare auto-discovered concepts to the 10 manually defined ones, measure overlap.

---

### Research 2: Graph Database for the Knowledge Graph

**Question**: Should the KG/MDG move from flat JSON files to a graph database?

**Options to evaluate**:
| Option | Pros | Cons |
|:---|:---|:---|
| **JSON files** (current) | Simple, portable, git-trackable | O(n) traversal, no query language |
| **SQLite + adjacency** | Local, no server, SQL queries | Not a native graph model |
| **Neo4j** | Purpose-built, Cypher queries, visualization | Requires server, heavy dependency |
| **NetworkX** (Python lib) | In-process graph, algorithms included | No persistence, memory-bound |

**Recommendation**: Start with **NetworkX** for in-process analysis (no new infrastructure), export to JSON for persistence. Move to Neo4j only if query complexity demands it.

**Research path**: Benchmark MDG traversal time at 100, 1000, and 10000 edges in JSON vs. NetworkX.

---

### Research 3: Temporal Snapshots via Git

**Question**: Can we use git itself as the temporal storage layer?

**Approach**:
- After each `intent_index_builder.py` run, commit `INTENT_INDEX.json` to a governance branch
- To query historical state: `git show governance-snapshots~5:INTENT_INDEX.json`
- Alignment score trends become `git log --format` queries

**Advantages**: No new infrastructure. Git already handles versioning, diffing, and time-stamping.

**Risk**: Large JSON files create noisy diffs. Consider storing only the summary section in git, with full index as an artifact.

**Research path**: Prototype a `scripts/snapshot.py` that commits the current index with a timestamped tag.

---

### Research 4: Governance-Aware Agent Instructions

**Question**: How does the governance engine feed into agent instructions at runtime?

**Concept**: When AXiomEngine assists with a codebase, the agent's system prompt should include:
- Active DataConcepts for the files in scope
- Active Decisions constraining the scope
- MDG pre-flight results

This turns the governance engine from a reporting tool into a **live constraint feed** for AI agents.

**Research path**:
1. Define a `governance_context.md` template that the agent system prompt includes
2. Populate it dynamically from `INTENT_INDEX.json` based on the files the agent is touching
3. Test whether agents actually respect the constraints (measure compliance rate)

---

### Research 5: Cross-Layer Rule Inference

**Question**: Can we automatically infer rules from observed behavior?

**Example**: If Reversa consistently finds that a validation rejects values > 180, and no PDD rule explicitly states this, the engine could propose:
```
Proposed Rule: R-INFERRED-MEMBERSHIP-MAX-180
Confidence: Inferred (from Reversa finding RF-001)
Status: PENDING_HUMAN_REVIEW
```

This bridges the gap between L2 (what code does) and L3 (what rules say it should do).

**Risk**: Inferred ≠ Authoritative. Must be clearly labeled and human-gated.

**Research path**: Build a `scripts/rule_inferrer.py` that diffs L2 findings against L3 rules and proposes candidates.

---

### Research 6: Governance Debt Quantification

**Question**: Can we produce a single number that represents "how much governance work remains?"

**Formula sketch**:
```
File Debt = code_chars × (1.0 - alignment_score) × complexity_weight
Project Debt = Σ(File Debt) / Total Code Chars
```

Where `complexity_weight` accounts for:
- Number of downstream MDG dependencies (higher = more critical)
- Whether the file has active Decisions (governed files are higher stakes)
- Language complexity (TypeScript > JSON)

**Value**: Enables tracking governance progress over time with a single trend line.

**Research path**: Compute debt scores for the current AXiomEngine codebase, validate that the ranking matches intuition about which files matter most.

---

## Suggested Execution Order

| Phase | What | Effort | Impact |
|:---|:---|:---|:---|
| **Now** | Fix 4: Exclusions | 30 min | Removes false noise immediately |
| **Now** | Fix 5: Decision capture CLI | 1 hour | Lowers barrier to hardest layer |
| **Next** | Fix 1: Explicit bindings | 2 hours | Makes alignment scores meaningful |
| **Next** | Fix 3: CLI portability | 2 hours | Enables use on other apps |
| **Soon** | Fix 2: Conflict detector | 3 hours | Surfaces highest-value governance signals |
| **Research** | R3: Git temporal snapshots | 1 hour pilot | Enables "was this correct then?" |
| **Research** | R4: Agent instruction feed | 2 hours pilot | Makes governance live, not just reported |
| **Research** | R1: Auto DataConcept discovery | 3 hours pilot | Reduces manual concept definition work |
| **Later** | R2: Graph database evaluation | Research only | Needed when MDG exceeds ~1000 edges |
| **Later** | R5: Cross-layer rule inference | Research + pilot | Bridges L2→L3 gap automatically |
| **Later** | R6: Governance debt metric | 1 hour | Executive-level tracking |

# 13-Layer Governance Engine — Workflow Guide

## Overview

This engine provides a **reusable, application-agnostic governance toolkit** that can be deployed against any codebase to analytically measure the alignment between human intent, governance rules, and code implementation.

AXiomEngine is the proving ground — the engine is built here, but designed to work on any application.

---

## Core Workflow: First-Time Onboarding

Use this workflow when applying the governance engine to a **new application** for the first time.

### Step 1: Establish Code Reality (L1)

**What**: Scan the target codebase to establish baseline metrics.

```bash
# The governance report provides L1 data (lines, chars, language per file)
# For AXiomEngine this already exists as AXIOMENGINE_GOVERNANCE_REPORT.md
# For a new app, generate one with the existing audit tooling
```

**Output**: A file inventory with line counts, character counts, and language detection.

**Who**: Developer or CI system  
**Time**: Automated, < 5 minutes  

---

### Step 2: Run Reversa Extraction (L2)

**What**: Use Reversa agents to extract behavioral specifications from the existing code.

```bash
# Install Reversa (one-time)
npx reversa install

# Run the analysis (in VS Code with Copilot/agent active)
/reversa
```

**Output**: `_reversa_sdd/` directory containing:
- Extracted business rules
- Control flow analysis
- Confidence-graded findings (Confirmed / Inferred / Gap)

**Who**: Developer with AI agent access  
**Time**: 30 min – 2 hours depending on codebase size  

> [!IMPORTANT]
> Reversa outputs are **descriptive, not authoritative**. They describe what the code does, not what it should do. Never treat them as policy.

---

### Step 3: Define DataConcepts (L8)

**What**: Identify the core **ideas** in the application. Not fields, not tables — concepts.

Edit `data/data_concepts.json`:

```json
{
  "concepts": [
    {
      "data_concept_id": "DC-YOUR-CONCEPT-HERE",
      "name": "Human-Readable Name",
      "definition": "What this concept represents in the domain",
      "status": "Active",
      "aliases": ["keyword1", "keyword2", "filename_match"]
    }
  ]
}
```

**Guidance**:
- Start with 5–10 concepts that represent the most critical domain ideas
- Aliases should match file names, function names, or module names in the codebase
- Every other layer attaches to these anchors

**Who**: Domain expert or governance analyst  
**Time**: 1–2 hours for initial set  

---

### Step 4: Extract PDD Rules (L3)

**What**: Decompose specifications, requirements, or documented obligations into atomic rules.

Rules are stored in `pdd/load_rules.py` (inline) or as entries in the Global Implementation Queue.

Each rule must have:
- **Stable ID** (e.g., `R-APP-FEATURE-001`)
- **Modality**: MUST / MUST_NOT / SHOULD / MAY
- **Scope**: What DataConcept it governs
- **Source**: Where this rule comes from

**Who**: PDD Author / Governance Analyst  
**Time**: 30–60 minutes per rule cluster  

---

### Step 5: Capture Decisions (L6)

**What**: Document governance decisions that are **not** in law, specs, or code — but are authoritative.

Edit `data/decisions.json`:

```json
{
  "decisions": [
    {
      "decision_id": "DEC-YOUR-APP-001",
      "decision_type": "Interpretation",
      "scope": {
        "applies_to": [
          {"entity_type": "DataConcept", "entity_id": "DC-YOUR-CONCEPT"}
        ]
      },
      "authority": {
        "body": "Who approved this",
        "evidence_ref": "Email/meeting/commit reference"
      },
      "rationale": "Why this decision was made (REQUIRED)",
      "effective": {
        "start_date": "2026-01-01",
        "end_date": null
      },
      "enforcement_guidance": {
        "enforcement_mode": "Strict",
        "system_expectation": "What systems MUST do"
      }
    }
  ]
}
```

> [!WARNING]
> Decisions are the **hardest layer to automate** and the **most dangerous to skip**. Without them, Reversa findings get classified as "wrong" instead of "superseded by decision."

**Who**: Governance lead, project owner  
**Time**: 10–15 minutes per decision  

---

### Step 6: Build Intent Index (All Layers)

**What**: Run the 13-layer engine to index every file against all governance layers.

```bash
python3 scripts/intent_index_builder.py
```

**Output**: `INTENT_INDEX.json` — every file annotated with its full 13-layer governance stack.

---

### Step 7: Build MDG (Materialized Dependencies)

**What**: Pre-compute dependency chains so impact analysis is O(1).

```bash
python3 scripts/mdg_builder.py
```

**Output**: `MDG.json` — nodes (DataConcepts, Rules, Decisions) and edges (REQUIRES, INTERPRETS, IMPLEMENTED_BY).

---

### Step 8: Generate Drift Report

**What**: Produce a human-readable governance analysis.

```bash
python3 scripts/drift_detector.py
```

**Output**: `GOVERNANCE_DRIFT_REPORT.md` — 13-layer coverage heatmap, component alignment, top drift risks, intent gaps.

---

## Operational Workflow: Before Making Changes

Use this workflow **every time** an agent or developer is about to modify governed code.

### Pre-Flight Check

```bash
# Check by DataConcept
python3 scripts/mdg_preflight.py DC-GPU-THERMAL-LIMIT

# Check by file
python3 scripts/mdg_preflight.py scripts/gpu_thermal_optimizer.py
```

**Interpret Results**:
- 🟢 **PASS**: No blocking dependencies. Proceed.
- 🟡 **WARN**: Active decisions constrain this scope. Review them before proceeding.
- 🔴 **FAIL**: High downstream impact. Must acknowledge all listed dependencies.

> [!CAUTION]
> If pre-flight returns FAIL, the agent **MUST stop** and present the dependency list to a human for review. This is the "stop-the-line" principle from PDD.

---

## Operational Workflow: After Making Changes

### Refresh Cycle

```bash
# 1. Rebuild the Intent Index (picks up new files, rules, concepts)
python3 scripts/intent_index_builder.py

# 2. Rebuild the MDG (picks up new dependency edges)
python3 scripts/mdg_builder.py

# 3. Regenerate drift report
python3 scripts/drift_detector.py
```

**When to run**:
- After adding new DataConcepts or Decisions
- After code deployment
- After PDD rule changes
- After Reversa re-extraction

---

## Layer Population Priority

Not all layers need to be filled at once. Here is the recommended priority:

| Priority | Layer | Why |
|:---|:---|:---|
| 🔴 Critical | L8 DataConcepts | Everything anchors to these — nothing works without them |
| 🔴 Critical | L3 PDD Rules | Defines what MUST/MUST_NOT happen |
| 🟡 High | L6 Decisions | Prevents misclassification of intentional overrides |
| 🟡 High | L2 Reversa | Surfaces what code actually does vs. what it should do |
| 🟢 Medium | L4 Authority | Classifies rules by authorization type |
| 🟢 Medium | L7 Obligations | Defines who is responsible for what |
| 🟢 Medium | L5 Derived Logic | Maps computed/inferred values |
| 🔵 Later | L9 Knowledge Graph | Expands structural dependency coverage |
| 🔵 Later | L11 Validation | Types rules as fatal/warning/informational |
| 🔵 Later | L12 Temporal | Adds time-scoping to all relationships |
| 🔵 Later | L10 MDG | Automatically built from other layers |
| 🔵 Later | L13 Process | Defines how governance stays correct over time |

---

## File Reference

| File | Purpose | Run |
|:---|:---|:---|
| `data/governance_schema.yaml` | Canonical 13-layer schema definition | Reference only |
| `data/data_concepts.json` | DataConcept anchor definitions | Edit manually |
| `data/decisions.json` | Governance decision records | Edit manually |
| `data/process_records/core_processes.yaml` | Process & provenance records | Edit manually |
| `pdd/load_rules.py` | PDD axiomatic rules | Edit manually |
| `scripts/intent_index_builder.py` | Build the 13-layer Intent Index | `python3 scripts/intent_index_builder.py` |
| `scripts/mdg_builder.py` | Build the Materialized Dependency Graph | `python3 scripts/mdg_builder.py` |
| `scripts/mdg_preflight.py` | Pre-flight check for changes | `python3 scripts/mdg_preflight.py <target>` |
| `scripts/drift_detector.py` | Generate drift analysis report | `python3 scripts/drift_detector.py` |
| `INTENT_INDEX.json` | Generated: per-file 13-layer governance data | Auto-generated |
| `MDG.json` | Generated: materialized dependency graph | Auto-generated |
| `GOVERNANCE_DRIFT_REPORT.md` | Generated: human-readable drift analysis | Auto-generated |

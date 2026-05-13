# 13-Layer Governance Engine — Suggested Use Cases

## What This Engine Is For

This engine answers one question across any codebase:

> **For any piece of code, what was the intent, what rules govern it, who decided what, and has it drifted from its purpose?**

It is designed to be deployed by AXiomEngine when assisting with building, rebuilding, or adding features to applications. Below are the primary use cases, ordered by immediate value.

---

## Use Case 1: New Feature Impact Analysis

**Scenario**: A developer or agent is adding a new feature to an existing application.

**Problem Without Governance**: The agent doesn't know what downstream systems depend on the files being modified. Changes break things silently.

**With the Engine**:
```bash
# Before making any changes, run pre-flight
python3 scripts/mdg_preflight.py path/to/file_being_changed.py
```

The MDG pre-flight returns:
- All downstream dependencies
- Any active governance decisions constraining the scope
- Required acknowledgements before proceeding

**Value**: Prevents "clever but unsafe" agent behavior. The agent **consults** dependencies instead of **discovering** them at runtime.

---

## Use Case 2: Legacy System Reverse Engineering

**Scenario**: An organization has a legacy application with tribal knowledge trapped in code. No one knows why certain logic exists.

**Workflow**:
1. Run Reversa against the codebase → surfaces behavioral truth (L2)
2. Define DataConcepts → anchors for what the system is about (L8)
3. Capture known governance decisions from stakeholders (L6)
4. Build the Intent Index → shows which code has known intent vs. dark spots
5. Generate drift report → identifies highest-risk areas

**Value**: Transforms "we think this is how it works" into "we can explain and prove why the system does what it does."

---

## Use Case 3: Compliance & Audit Defense

**Scenario**: An auditor asks "Why does your system collect this data?" or "Was this behavior correct on March 15, 2025?"

**With the Engine**:
- **L4 (Authority)** answers: "Under what law/rule/policy is this authorized?"
- **L6 (Decisions)** answers: "What governance decisions were in effect?"
- **L12 (Temporal)** answers: "What was the state at that point in time?"
- **L13 (Process)** answers: "How was this information obtained and validated?"

**Value**: Audit responses become deterministic lookups instead of forensic archaeology.

---

## Use Case 4: Safe AI-Assisted Code Generation

**Scenario**: An AI agent is generating code for a governed system. How do you prevent it from violating rules it doesn't know about?

**Workflow**:
1. Agent receives a task
2. Agent queries the Intent Index for the target scope
3. MDG pre-flight identifies constraints and decisions
4. Agent generates code **within** the declared governance boundaries
5. Post-generation, the drift detector verifies alignment hasn't degraded

**PDD Pipeline Integration**:
```
Prompt → Intent Retrieval → MDG Pre-Flight → Execute → Review → Drift Check
                                    ↑
                              MANDATORY GATE
```

**Value**: AI agents become **structurally constrained**, not just "careful." The difference between clever and safe.

---

## Use Case 5: Application Rebuild / Migration

**Scenario**: An application is being rebuilt from scratch, or migrated to a new technology stack. The new system must preserve all existing business rules.

**Workflow**:
1. Run full governance scan on the old system (all 13 layers)
2. Extract every DataConcept, Rule, Decision, and Obligation
3. Use the Intent Index as the **specification** for the new system
4. As the new system is built, re-run the engine to measure coverage
5. The drift report shows which original business rules have been reimplemented vs. lost

**Value**: Migration completeness becomes measurable, not aspirational.

---

## Use Case 6: Multi-Application Governance Comparison

**Scenario**: An organization runs multiple applications that should follow the same governance standards.

**Workflow**:
1. Run the engine against each application independently
2. Compare drift reports side-by-side
3. Identify which applications have governance gaps
4. Share DataConcepts and PDD rules across applications where applicable

**Value**: Governance maturity becomes comparable across an entire portfolio.

---

## Use Case 7: Change Propagation Tracking

**Scenario**: A law changes, a policy is updated, or a governance decision is revised. What code needs to change?

**With the MDG**:
```bash
# "What is affected if this law changes?"
python3 scripts/mdg_preflight.py LAW-UT-ATTENDANCE-001

# "What depends on this DataConcept?"
python3 scripts/mdg_preflight.py DC-STUDENT-MEMBERSHIP-DAYS
```

The MDG traces the full dependency chain:
```
Law → DataConcept → PDD Rule → Validation → Code
```

**Value**: Change impact analysis is O(1) — a graph query, not a human investigation.

---

## Use Case 8: Onboarding New Team Members

**Scenario**: A new developer joins a project and needs to understand what the system does and why.

**With the Engine**:
- **Drift Report**: Shows the system's governance health at a glance
- **DataConcepts**: Lists the core domain ideas
- **Decisions**: Explains why certain things are the way they are
- **Intent Index**: Per-file governance stack answers "why does this file exist?"

**Value**: Reduces onboarding from weeks of tribal knowledge transfer to hours of structured reading.

---

## Maturity Model

Organizations using this engine will progress through these stages:

| Stage | Description | Typical Alignment Score |
|:---|:---|:---|
| **0 — Dark** | No governance data. Code exists but nothing is known about it. | 0.00 – 0.08 |
| **1 — Scanned** | L1 (Code) measured. Basic file inventory exists. | 0.08 – 0.15 |
| **2 — Extracted** | L2 (Reversa) run. Behavioral truth surfaced. | 0.15 – 0.25 |
| **3 — Anchored** | L8 (DataConcepts) defined. Core ideas identified. | 0.25 – 0.40 |
| **4 — Governed** | L3 (Rules) + L6 (Decisions) populated. Intent is explicit. | 0.40 – 0.60 |
| **5 — Enforced** | L10 (MDG) + Pre-flight checks active. Changes are gated. | 0.60 – 0.80 |
| **6 — Auditable** | L12 (Temporal) + L13 (Process) complete. Point-in-time replay possible. | 0.80 – 1.00 |

**AXiomEngine Current Stage**: **Stage 2–3** (Mean Alignment: 0.202, 10 DataConcepts seeded)

---

## Quick Reference: Command Cheat Sheet

```bash
# Build everything from scratch
python3 scripts/intent_index_builder.py  # Index all 13 layers
python3 scripts/mdg_builder.py           # Build dependency graph
python3 scripts/drift_detector.py        # Generate drift report

# Pre-flight before changes
python3 scripts/mdg_preflight.py DC-GPU-THERMAL-LIMIT      # By concept
python3 scripts/mdg_preflight.py scripts/some_file.py      # By file
python3 scripts/mdg_preflight.py R-PDD-CORE-001            # By rule
python3 scripts/mdg_preflight.py DEC-P40-POWER-LIMIT-150W  # By decision

# Edit governance data
vim data/data_concepts.json              # Add/edit DataConcepts
vim data/decisions.json                  # Add/edit Decisions
vim data/process_records/core_processes.yaml  # Add/edit ProcessRecords
```

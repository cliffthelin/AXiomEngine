# Purpose and Scope

This document externalizes authoritative business logic and decision rules for the current system or domain. These rules may define eligibility logic, validation requirements, thresholds, classifications, state transitions, matching rules, or other operational constraints. AI agents must retrieve these rules before modifying behavior that depends on business logic; they must never infer or redefine business rules from code patterns alone.

## Non-Goals (Explicit Constraints)

**

### R-BUSINESS-NG-005
Never Invent Existing Infrastructure or Data Assets**
- Do not invent servers, hostnames, environments, databases, schemas, tables, columns, fields, indexes, queues, topics, APIs, or external systems when describing the current or legacy reality.
- Every existing infrastructure or data asset named as factual must be backed by direct evidence from code, configuration, SQL, migrations, manifests, logs, or other retrieved artifacts.
- If exact evidence is missing, mark the claim as a gap or uncertainty instead of filling it in from patterns.
- Near matches, naming conventions, or common enterprise defaults are not authority.
- You may propose new solution objects when the task is design, planning, migration, or implementation, but they must be explicitly labeled as new, proposed, target-state, or to-be-created rather than implied to already exist.

**

### R-BUSINESS-NG-006
Factual Traceability Over Completeness**
- In provenance-enabled workflows, every confirmed statement about the existing system must point to factual evidence.
- If a field, table, database, or server cannot be tied to retrieved evidence, the statement must not be marked confirmed as existing.
- Proposed new design objects do not require historical evidence, but they must be traceable to the requirement, plan, or design decision that introduced them.
- Prefer an explicit omission or 🔴 GAP over a plausible but unverified detail when speaking about the current system.

## 

## Usage Notes for AI Agents

When modifying business-logic-bearing code, workflows, data transformations, rules engines, validations, or decision flows:
1. **Read this document first** before suggesting changes to logic governed by business policy
2. **Reference rule IDs** in code comments, specs, or decision notes when the environment supports it
3. **Do not infer** new business rules from code patterns; retrieve them from authoritative documentation
4. **If rules are missing**: Halt execution and request documentation update, do not guess
5. **If rules conflict**: Stop-the-line (R-SYS-003), request clarification from human authority

## 

## Maintenance

This section must be updated when:
- New business conditions or decision criteria are introduced
- Thresholds, classifications, or state-transition rules are changed
- Validation rules are added or modified
- New hardcoded logic, constants, or "magic numbers" are discovered in business-critical code

Implementation code should reference these rules, not redefine them.
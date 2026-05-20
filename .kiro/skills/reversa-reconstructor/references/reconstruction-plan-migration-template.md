```markdown
# Reconstruction Plan — {{PROJECT_NAME}}

**Source:** migration
**Target Paradigm:** {{PARADIGM}}
**Topology:** {{TOPOLOGY}}
**Stack:** {{STACK}}
**Strategy:** {{STRATEGY}}
**Generated on:** {{DATE}}
**Status:** {{TOTAL}} tasks | {{DONE}} completed | {{PENDING}} pending

---

## Pre-Flight Checks

> Review before starting. Items REFERENCED IN CODE in `ambiguity_log.md` that affect specific tasks are marked.

{{#each PREFLIGHT_ALERTS}}
- ⚠️ **{{this.item}}** — affects Task {{this.task_number}} ({{this.task_name}}). Source: `_reversa_sdd/migration/ambiguity_log.md`
{{/each}}

{{#if NO_ALERTS}}
No blocking items. You can start.
{{/if}}

---

## Tasks

### Task 01 — New Project Setup
**Status:** pending
**Reads:** `_reversa_sdd/migration/topology_decision.md`, `_reversa_sdd/migration/paradigm_decision.md`
**Builds:** initial folder/module structure, base configuration, minimum dependencies
**Ready when:** the skeleton of the new repository matches the approved topology and chosen paradigm

---

### Task 02 — Target Database Schema
**Status:** pending
**Reads:** `_reversa_sdd/migration/target_data_model.md`
**Builds:** migrations, schema, ORM models (based on stack)
**Ready when:** all tables/collections of the target data model exist with correct types, constraints, and relationships

---

### Task 03 — Data Migration Plan
**Status:** pending
**Reads:** `_reversa_sdd/migration/data_migration_plan.md`, `_reversa_sdd/migration/target_data_model.md`
**Builds:** ETL scripts/jobs, integrity validations, rollback
**Ready when:** migration scripts tested with a representative volume, validations match the plan
**Note:** Skip if the strategy in `migration_strategy.md` does not involve data migration (e.g., completely new system from scratch without legacy data)

---

### Task 04 — Target Domain Entities
**Status:** pending
**Reads:** `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Builds:** entities, value objects, aggregates, business rules
**Ready when:** domain implemented according to the target model, business rules covered by tests

---

<!-- MODULE_TASKS_START -->
<!-- The Reconstructor inserts a task per module identified in target_architecture.md, in dependency order. -->
<!-- Example: -->

### Task 05 — [Module Name]
**Status:** pending
**Reads:** `_reversa_sdd/migration/target_architecture.md` (section `[module]`), `_reversa_sdd/migration/target_domain_model.md`, `_reversa_sdd/migration/target_business_rules.md`
**Builds:** [module path according to the approved topology]
**Ready when:** [parity criterion extracted from parity_specs.md, if applicable; otherwise, criterion in target_architecture.md]
**Alert:** [if there is an item REFERENCED IN CODE associated]

<!-- MODULE_TASKS_END -->

---

### Task {{CUTOVER_N}} — Cutover
**Status:** pending
**Reads:** `_reversa_sdd/migration/cutover_plan.md`
**Builds:** cutover scripts/checklists, traffic switch, executable rollback plan
**Ready when:** the new system receives traffic according to the plan, and the legacy system can be shut down/frozen as decided

---

### Task {{PARITY_N}} — Parity Validation
**Status:** pending
**Reads:** `_reversa_sdd/migration/parity_specs.md`, `_reversa_sdd/migration/parity_tests/[list of .feature files]`
**Builds:** parity test suite running against legacy and new, divergence report
**Ready when:** all critical flows defined in parity_specs.md pass in both systems with equivalent results
```
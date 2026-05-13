# Reconstruction Plan — {{PROJECT_NAME}}

**Stack:** {{STACK}}
**Generated on:** {{DATE}}
**Status:** {{TOTAL}} tasks | {{DONE}} completed | {{PENDING}} pending

---

## Pre-Flight Checks

> Review these points before starting. Issues marked with ⚠️ block the associated task.

{{#each PREFLIGHT_ALERTS}}
- ⚠️ **{{this.gap}}** — blocks Task {{this.task_number}} ({{this.task_name}})
{{/each}}

{{#if NO_ALERTS}}
No critical issues identified. You can safely proceed.
{{/if}}

---

## Tasks

### Task 01 — Database Schema
**Status:** pending
**Reads:** `_reversa_sdd/erd-complete.md`, `_reversa_sdd/data-dictionary.md`
**Builds:** migrations, schema, ORM models (based on detected stack)
**Ready when:** All tables in the ERD exist with correct types, constraints, and foreign keys

---

### Task 02 — Domain Entities
**Status:** pending
**Reads:** `_reversa_sdd/domain.md`, `_reversa_sdd/data-dictionary.md`
**Builds:** entities, value objects, domain validations
**Ready when:** All entities are implemented with the described business rules

---

### Task 03 — State Machines
**Status:** pending
**Reads:** `_reversa_sdd/state-machines.md`
**Builds:** implementation of the state flows for each entity
**Ready when:** All documented states and transitions are implemented
**Note:** Skip this task if `_reversa_sdd/state-machines.md` does not exist

---

<!-- COMPONENT_TASKS_START -->
<!-- The Reconstructor inserts a task for each unit here, in the bottom-up order determined by dependencies.md -->
<!-- Example of a unit task: -->

### Task 04 — [Unit Name]
**Status:** pending
**Reads:** `_reversa_sdd/[unit]/requirements.md`, `_reversa_sdd/[unit]/design.md`, `_reversa_sdd/[unit]/tasks.md`, `_reversa_sdd/dependencies.md`
**Builds:** [module path based on stack]
**Ready when:** [acceptance criteria extracted from requirements.md, "Given/When/Then" field]
**Alert:** [if there is an associated issue, describe it here]

<!-- COMPONENT_TASKS_END -->

---

### Task {{API_N}} — API Layer
**Status:** pending
**Reads:** `_reversa_sdd/openapi/[list of files]`
**Builds:** endpoints, controllers, middlewares, authentication
**Ready when:** All endpoints respond according to the OpenAPI contracts

---

### Task {{STORIES_N}} — User Flows
**Status:** pending
**Reads:** `_reversa_sdd/user-stories/[list of files]`
**Builds:** end-to-end integration, complete user flows
**Ready when:** All acceptance criteria of the user stories are met
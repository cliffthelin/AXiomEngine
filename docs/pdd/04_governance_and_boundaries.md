# Purpose and Scope

This document establishes role boundaries, standardization, and the organizational source of truth. 

### R-PDD-GOV-001
Single Source of Truth Authoritative organizational intent lives in exactly one maintained system of Markdown artifacts. If two documents disagree, only one is allowed to be authoritative. 

### R-PDD-GOV-002
Role Boundaries To prevent governance collapse, no actor may author, execute, and approve the same change. Roles are defined by actions:
- Intent Author: Defines authoritative Markdown and rules.
- Executor (Human or Agent): Produces outputs that comply strictly with intent. AI agents must never author or mutate intent.
- Reviewer / Validator: Compares outputs against intent; cannot generate fixes.
- Governor: Enforces pipeline boundaries and halts violations. 

### R-PDD-GOV-003
Interface Standardization Governance standardizes rule identifiers, required structural anchors, and validation semantics. It must not standardize prose style or domain abstractions.
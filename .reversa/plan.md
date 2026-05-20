# Exploration Plan — AXiomEngine

> Created by Reversa on 2026-05-20
> Mark each task with ✅ when completed.
> You can edit this plan before starting: add, remove, or reorder tasks as needed.

---

## Phase 1: Reconnaissance 🔍

- [ ] **Scout** — Mapping of folder structure and technologies
- [ ] **Scout** — Analysis of dependencies and package managers
- [ ] **Scout** — Identification of entry points, CI/CD, and configurations

## Decision on organization of specs 🗂️

> Between the Scout and the Archaeologist steps, Reversa will ask you how you want to organize the specs (by module, use case, endpoint, hybrid, by features, or custom). This choice is persisted in `.reversa/config.toml` in the `[specs]` section and will not be asked again in future runs. To re-present the menu, manually remove the section.

## Phase 2: Excavation 🏗️

> Reversa will populate this section with the actual modules after the Scout completes the reconnaissance.

- [ ] **Archaeologist** — Analysis of the modules identified by the Scout

## Phase 3: Interpretation 🧠

- [ ] **Detective** — Git archaeology and retroactive ADRs
- [ ] **Detective** — Implicit business rules and state machines
- [ ] **Detective** — Permissions matrix (RBAC/ACL)
- [ ] **Architect** — C4 diagrams (Context, Containers, Components)
- [ ] **Architect** — Complete ERD and external integrations
- [ ] **Architect** — Spec Impact Matrix

## Phase 4: Generation 📝

- [ ] **Writer** — SDD specs per component
- [ ] **Writer** — OpenAPI (if applicable)
- [ ] **Writer** — User Stories (if applicable)
- [ ] **Writer** — Code/Spec Matrix

## Phase 5: Review ✅

- [ ] **Reviewer** — Cross-review of specs
- [ ] **Reviewer** — Resolution of gaps with the user
- [ ] **Reviewer** — Final confidence report

---

## Independent Agents

> Run these agents when resources are available — they can run at any phase.

- [ ] **Viewer** — Interface analysis via screenshots
- [ ] **Data Master** — Complete database analysis
- [ ] **Design System** — Extraction of design tokens
- [ ] **Tracer** — Dynamic analysis (requires accessible system)

---

## Next Step

After the Discovery Team completes its work and `_reversa_sdd/` is populated, you can trigger one of the following flows:

- `/reversa-migrate`: orchestrator for the **Migration Team** (Paradigm Advisor → Curator → Strategist → Designer → Screen Translator → Inspector). Generates the specs for the new system. Output in `_reversa_sdd/migration/` and `_reversa_sdd/screens/`.
- `/reversa-reconstructor`: generates a bottom-up plan to reimplement the software from the legacy specs (one task per session).
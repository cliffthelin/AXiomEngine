```markdown
---
name: reversa-agents-help
description: Explains, using analogies, what each Reversa agent does and when to use it. Activate with /reversa-agents-help.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  role: help
---

Present exactly the text below, without changes, without summarizing.

---

# Reversa Agents — Guide with Analogies

Reversa is a team of specialists. Each agent does only one thing — and does it well.

---

## 🎼 Reversa — Central Orchestrator
**Command:** `/reversa`

An orchestra conductor doesn't play any instrument. They know the entire score and tell who enters when, in what order, and at what tempo. Without them, each musician would play their part without connecting with the others.

> Use Reversa to start or resume the complete analysis. It manages the sequence for you.

---

## 🗺️ Scout — The Real Estate Agent
**Command:** `/reversa-scout`

The real estate agent takes the first tour of the property. They don't open drawers, don't read documents, don't touch anything. They just map: how many rooms, what neighborhood, what installations exist, what is the general state.

> Use Scout at the beginning. It generates the project inventory — languages, frameworks, modules, dependencies — without going into the code.

---

## 🧬 Soul Extractor: The Express Biographer
**Command:** `/reversa-extract-soul`

The express biographer visits the subject, reads the notes from the real estate agent (Scout), quickly browses a few family albums and the history of letters (git log), and produces a one-page biography: who they are, what they do, and the founding decisions that shaped their entire life. It's not the complete story, it's the distilled soul.

> Use Soul Extractor immediately after Scout, when you want an executive summary of the system (purpose, central entities, and founding decisions) in a single Spec, without waiting for the entire pipeline. It doesn't replace Archaeologist or Detective.

---

## ⛏️ Archaeologist — The Excavator
**Command:** `/reversa-archaeologist`

The archaeologist excavates the terrain patiently, layer by layer. They catalog each artifact found: size, material, location, shape. They don't interpret the civilization, they simply describe precisely what is there.

> Use Archaeologist to analyze the code module by module. It extracts functions, algorithms, data structures, and control flows. **Run one module per session** to save tokens.

---

## 🔍 Detective — The Sherlock Holmes
**Command:** `/reversa-detective`

Sherlock Holmes arrives after the archaeologist. He looks at the cataloged artifacts and asks: *"But why is this here? Who put it here? What does this reveal about who lived here?"* He doesn't excavate. He interprets.

> Use Detective after Archaeologist. It extracts implicit business rules, reads the git history as a diary, and reconstructs decisions that no one documented.

---

## 📐 Architect — The Cartographer
**Command:** `/reversa-architect`

The cartographer visits a territory and produces formal maps: floor plan, elevation map, structural plan. Someone who has never been there can understand everything by looking at the maps.

> Use Architect after Detective. It synthesizes everything into C4 diagrams, a complete ERD, and an integration map.

---

## 📝 Writer — The Notary
**Command:** `/reversa-writer`

The notary transforms what was discovered into formal, precise, and traceable contracts. Each clause has a declared degree of certainty. The document serves as a contract: an AI agent can reimplement the system from it.

> Use Writer after Architect. It generates SDD specs, OpenAPI, and user stories with code traceability.

---

## ⚖️ Reviewer — The Spec Reviewer
**Command:** `/reversa-reviewer`

The Reviewer takes the contracts from the Writer and tries to break them: *"This is a contradiction. This point has no evidence. This rule fails if the user does X."* They don't want to destroy, they want to ensure that what remains is solid.

> Use Reviewer after Writer. It critically reviews the specs, reclassifies confidence, and raises questions for human validation.

---

## 🖼️ Visor — The Forensic Illustrator
**Command:** `/reversa-visor`

The forensic illustrator works only with images. They receive screenshots of the system and faithfully reconstruct the interface: screens, forms, navigation flows. It doesn't need the system to be running — only the photos.

> Use Visor when screenshots are available. It documents the GI without needing access to the system.

---

## 🗄️ Data Master — The Geologist
**Command:** `/reversa-data-master`

The geologist maps the underground — the layer that no one sees but that supports everything. Tables, relationships, constraints, triggers, procedures. The invisible foundation upon which the application is built.

> Use Data Master when DDL, migrations, or ORM models are available. It documents the database completely.

---

## 🎨 Design System — The Stylist
**Command:** `/reversa-design-system`

The stylist catalogs the wardrobe: color palette, typography, spacing, design tokens. The "fashion rules" that govern the appearance of the system — what can and cannot be combined.

> Use Design System when CSS files, themes, or screenshots of the interface are available. It extracts the visual tokens of the project.

---

## Recommended Sequence

```
/reversa → orchestrates everything automatically

Or manually:
Scout → Archaeologist (N sessions) → Detective → Architect → Writer → Reviewer

Optional at any stage:
Soul Extractor · Visor · Data Master · Design System
```

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

# Reversa Agents – Guide with Analogies

Reversa is a team of specialists. Each agent does only one thing – and does it well.

---

## 🎼 Reversa – Central Orchestrator
**Command:** `/reversa`

An orchestra conductor doesn't play any instruments. They know the entire score and tell everyone when to start, in what order, in what rhythm. Without them, each musician would play their part without connecting with the others.

> Use Reversa to start or resume the complete analysis. It takes care of the sequence for you.

---

## 🗺️ Scout – The Real Estate Agent
**Command:** `/reversa-scout`

The real estate agent takes the first tour of the property. Doesn't open drawers, doesn't read documents, doesn't touch anything. Just maps: how many rooms, what is the neighborhood, what are the existing installations, what is the overall condition.

> Use the Scout at the beginning. It generates the project inventory – languages, frameworks, modules, dependencies – without entering the code.

---

## 🧬 Soul Extractor: The Express Biographer
**Command:** `/reversa-extract-soul`

The express biographer visits the subject, reads the notes from the real estate agent (Scout), quickly browses some family albums and the history (git log), and produces a one-page biography: who they are, what they do, and the foundational decisions that shaped their entire life. It's not the complete story; it's the distilled soul.

> Use the Soul Extractor immediately after the Scout when you want an executive summary of the system (purpose, core entities, and foundational decisions) in a single Spec, without waiting for the entire pipeline. It does not replace Archaeologist or Detective.

---

## ⛏️ Archaeologist – The Excavator
**Command:** `/reversa-archaeologist`

The archaeologist excavates the terrain patiently, layer by layer. Catalogs each artifact found: size, material, location, shape. They don't interpret the civilization; they only accurately describe what is there.

> Use the Archaeologist to analyze the code module by module. It extracts functions, algorithms, data structures, and control flows. **Run one module per session** to save tokens.

---

## 🔍 Detective – The Sherlock Holmes
**Command:** `/reversa-detective`

Sherlock Holmes arrives after the archaeologist. He looks at the cataloged artifacts and asks: *"But why is this here? Who put it here? What does this reveal about who lived here?"* He doesn't excavate. He interprets.

> Use the Detective after the Archaeologist. It extracts implicit business rules, reads the git history like a diary, and reconstructs decisions that no one documented.

---

## 📐 Architect – The Cartographer
**Command:** `/reversa-architect`

The cartographer visits a territory and produces formal maps: floor plan, elevation map, structural plan. Someone who has never set foot there can understand everything by looking at the maps.

> Use the Architect after the Detective. It synthesizes everything into C4 diagrams, a complete ERD, and integration map.

---

## 📝 Writer – The Notary
**Command:** `/reversa-writer`

The notary transforms what was discovered into formal, accurate, and traceable contracts. Each clause has a declared degree of certainty. The document serves as a contract: an AI agent can reimplement the system based on it.

> Use the Writer after the Architect. It generates the SDD specs, OpenAPI definitions, and user stories with code traceability.

---

## ⚖️ Reviewer – The Spec Reviewer
**Command:** `/reversa-reviewer`

The Reviewer takes the Writer's contracts and tries to break them: *"This is a contradiction. This point has no proof. This rule fails if the user does X."* It doesn't want to destroy; it wants to ensure that what remains is solid.

> Use the Reviewer after the Writer. It critically reviews the specs, reclassifies confidence levels, and raises questions for human validation.

---

## 🖼️ Visor – The Forensic Illustrator
**Command:** `/reversa-visor`

The forensic illustrator works only with images. It receives screenshots of the system and faithfully reconstructs the interface: screens, forms, navigation flows. It doesn't need the system to be running – just the photos.

> Use the Visor when screenshots are available. It documents the UI without requiring access to the system.

---

## 🗄️ Data Master – The Geologist
**Command:** `/reversa-data-master`

The geologist maps the underground – the layer that no one sees but that supports everything. Tables, relationships, constraints, triggers, procedures. The invisible foundation upon which the application is built.

> Use the Data Master when DDL, migrations, or ORM models are available. It completely documents the database.

---

## 🎨 Design System – The Stylist
**Command:** `/reversa-design-system`

The stylist catalogs the wardrobe: color palette, typography, spacing, design tokens. The "fashion rules" that govern the appearance of the system – what can and cannot be combined.

> Use the Design System when CSS files, themes, or interface screenshots are available. It extracts the project's visual tokens.

---

## Recommended Sequence

```
/reversa → orchestrates everything automatically

Or manually:
Scout → Archaeologist (N sessions) → Detective → Architect → Writer → Reviewer

Optional at any stage:
Soul Extractor · Visor · Data Master · Design System
```

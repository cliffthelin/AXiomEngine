```markdown
---
name: reversa-visor
description: Documents the legacy system interface based on screenshots – extracts components, layouts, navigation flows, and screen states. Use when screenshots of the system are available, without needing the system to be running.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills (requires image support in the model).
metadata:
  author: sandeco
  version: "1.1.0"
  framework: reversa
  phase: any
---

You are the Visor. Your mission is to document the interface from images, without requiring the system to be running.

## Before You Start

Read, in this order:

1. `.reversa/state.json` → `output_folder` field (default: `_reversa_sdd`).
2. `.reversa/config.toml` → `[specs]` section (`granularity`, `custom_folders` fields).
3. `.reversa/config.user.toml` → `[specs]` section if it exists, with key-by-key precedence.
4. `.reversa/context/surface.json` → `modules`, `organization_suggestion.features`.

`granularity` defines how each screen is mapped to a unit (see "Screen → Unit Mapping" below).

## User Prompt

If you don't already have screenshots:
> "[Name], to document the interface, please send screenshots of the system screens. You can send one at a time or multiple at once. Prioritize the main screens and the most important flows."

## Process

### 1. Screen Inventory

For each screenshot:

- Name and purpose of the screen.
- State (loading, empty, populated, error, confirmation).
- Context of use (how the user arrived here).

### 2. Interface Elements

**Forms:** fields (label, type, placeholder, required), visible validations, action buttons.

**Tables and Listings:** columns, actions per row, visible pagination, and filters.

**Navigation:** main menu, submenus, breadcrumbs, links.

**Feedback:** success/error/alert messages, modals, confirmations, tooltips.

### 3. Navigation Flow

- Map the navigation between screens.
- Identify main and alternative flows.
- Entry and exit points.

### 4. States

Compare the same screen in different states when possible (empty vs. populated, normal vs. error).

### 5. Screen → Unit Mapping

For each screen, decide to which unit it belongs. The unit follows the `granularity` read from `[specs]`:

| `granularity` | How to map the screen |
|---------------|---------------------|
| `module` | The screen's URL/route matches the name of a module in `surface.json.modules` (e.g., `/orders/...` → `pedidos`). |
| `endpoint` | The screen consumes a set of endpoints; choose the main endpoint as the unit. |
| `use-case` | The screen executes an identifiable use case; map it to the corresponding use case. |
| `hybrid` | Map at the most specific applicable level, either a nested module or use case. |
| `feature` | The screen is part of one of the features listed in `organization_suggestion.features`. |
| `custom` | The screen matches one of the folders in `[specs].custom_folders`. |

When the mapping is ambiguous (the screen belongs to two potential units), ask the user before saving.

When the unit folder does not yet exist (Writer has not run), create it empty to host the screenshots. The Writer, when running later, will find the folder and add `requirements.md`, `design.md`, `tasks.md` (EC-05).

## Output

**Per unit, within the unit folder:**

- `<output_folder>/<unit>/screenshots/<screen-name>.<ext>`, the original screenshot(s) captured by the user (RF-09).
- `<output_folder>/<unit>/screens.md`, detailed specification of the screens in this unit (one section per screen). Replaces the old `screens/<screen-name>.md` file.

**Globally, in the root of `<output_folder>/ui/`:**

- `inventory.md`, complete inventory of all screens, with the unit to which each was mapped.
- `flow.md`, navigation flow in Mermaid (traverses units).

## Non-Destructive Directive

Never delete or overwrite existing screenshots or specifications. If the user sends the same screen twice, save it with a numeric suffix (`screen.png`, `screen-2.png`).

Report to Reversa: documented screens (and the unit of each), and mapped flows.
```
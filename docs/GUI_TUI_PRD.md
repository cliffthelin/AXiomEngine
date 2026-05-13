# Product Requirements Document: UI Expansion (Web GUI & TUI)

## 1. Overview
The AXiomEngine ecosystem currently relies on a minimal Web GUI (`/admin/dashboard`, `/admin/settings`) and a CLI-based Terminal User Interface (`rich_tui.py`). Both interfaces currently lack the tooling needed for deep system observability, manual intervention, and live debugging. 

This PRD outlines the missing features and defines the requirements for implementing parity across both the Web GUI and the TUI.

---

## 2. Feature Definitions & Implementation Requirements

### Feature 1: Live Log Viewer
**Description:** Real-time streaming logs from the Stitch messaging bus, the Router, Valkey, and individual Agent Daemons.
* **Web GUI Implementation:** 
  * A dedicated `/admin/logs` page or a full-width "Terminal" component on the Dashboard.
  * Use WebSockets to stream standard out/err from the backend `tail -f` processes directly to the browser.
  * Color-coded formatting (Warnings in yellow, Errors in red, Agent outputs in blue).
* **TUI Implementation:** 
  * A new Rich `Panel` or hotkey (`L` for Logs) that splits the terminal view.
  * Integration with Python's `logging` module handlers to intercept live logs without breaking the chat interface.

### Feature 2: Agent Inspector (Fleet Manager)
**Description:** A monitoring interface that displays all active `agent_daemon.py` instances, their current VRAM utilization, their active tasks, and their state (Idle, Running, Offline).
* **Web GUI Implementation:** 
  * A "Fleet" or "Agents" tab on the Dashboard.
  * Visual cards for each active daemon showing: Name, Model Loaded, Current Task ID, Uptime, and a "Kill/Restart" action button.
* **TUI Implementation:**
  * A sidebar (like a buddy list) or a hotkey (`A` for Agents) that lists connected agents.
  * A command (e.g., `/agents`) to print a formatted Rich `Table` showing agent statuses pulled from Valkey's heartbeat registry.

### Feature 3: Model & VRAM Manager
**Description:** Operational control over the local LLM inference engines (Ollama & Split VGPU). Ability to view total VRAM pools, force-unload idle models, and preload models.
* **Web GUI Implementation:** 
  * A "VRAM & Models" dashboard utilizing the new `OllamaController` methods (`get_vram_usage()`, `list_running()`).
  * Progress bars showing VRAM capacity vs Usage.
  * "Unload" buttons next to running models.
* **TUI Implementation:**
  * A command (e.g., `/vram` or `/models`) that prints a Rich `Progress` bar showing memory allocation and a list of loaded models.
  * Commands to manipulate models (e.g., `/unload qwen3.6:27b`).

### Feature 4: Manual Rule & Policy Editor (PDD)
**Description:** Currently, the system only allows admins to Approve/Reject *proposals* made by agents. Admins need the ability to manually author, edit, and delete PDD governance rules.
* **Web GUI Implementation:** 
  * A "Rule Editor" modal or page connected to the Postgres `pdd_rules` table.
  * Syntax-highlighted text area for drafting rule definitions.
  * Enable/Disable toggle for bypassing the agent proposal pipeline.
* **TUI Implementation:**
  * A command (`/rule new`, `/rule edit <id>`) that drops the user into an interactive prompt to write a rule.
  * Print out active rules in a readable markdown format using Rich's Markdown renderer.

### Feature 5: Knowledge Graph Explorer
**Description:** A visual or hierarchical representation of the `knowledge_graph.json` so users can explore relationships and memory contexts without raw JSON parsing.
* **Web GUI Implementation:** 
  * Integration of a library like `vis.js` or `d3.js` to draw interactive force-directed graphs.
  * Clickable nodes that expand to show metadata and linked nodes.
* **TUI Implementation:**
  * Since 2D graphics aren't viable in the terminal, implement a hierarchical tree view using Rich's `Tree` component (`/kg show`).
  * Allow text-based search/querying of nodes (`/kg search <topic>`).

---

## 3. Prioritization & Phasing
**Phase 1: Observability (High Priority)**
* Agent Inspector (Web & TUI)
* Live Log Viewer (Web & TUI)

**Phase 2: Control (Medium Priority)**
* Model & VRAM Manager (Web & TUI)
* Manual Rule Editor (Web)

**Phase 3: Visualization (Low Priority)**
* Knowledge Graph Explorer (Web)

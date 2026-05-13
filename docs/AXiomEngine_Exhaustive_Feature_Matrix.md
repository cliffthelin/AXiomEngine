# Exhaustive System Feature & Governance Matrix

This document provides a low-level, comprehensive breakdown of every system, module, extension, and feature currently present in the AXiomEngine codebase. It explicitly maps what Governance Rules (PDD) apply to them, and identifies precisely where they are exposed (GUI, TUI, CLI, or Nowhere).

---

## 1. Core Systems & Agents

### 1.1. PI (Personal Intelligence)
*Files: `pi/pi.py`, `pi/pi_tui.py`*
* **Features:**
  * Interactive CLI chat loop for direct user querying.
  * Rich Dashboard TUI with live system metrics and markdown streaming.
  * Explicit command delegation (e.g., typing `plan` routes to Archon).
  * Auto-tagging of `["personal", "delegation"]` contexts.
* **Governing Rules:** `R-PDD-CORE-001` (AI Does Not Infer Intent), `R-PDD-CORE-003` (Developer is a Context Orchestrator).
* **Exposure:** 
  * **CLI:** ✅ (`pi/pi.py` using `agent_loop` & `pi_ai`)
  * **TUI:** ✅ (`pi/pi_tui.py` with live reasoning/thinking blocks)
  * **GUI:** ✅ (`/ws/agent` WebSocket streaming to Dashboard)

### 1.2. Archon (Architecture & Planning Agent)
*Files: `archon/archon.py`, `scripts/agent_daemon.py`*
* **Features:**
  * Autonomous task breakdown and workflow orchestration.
  * Emits component-level subtasks into the Stitch bus.
* **Governing Rules:** `R-PDD-ATLAS-001` (AI Atlas Code Engineering), `R-PDD-SYMPHONY-001` (Autonomous Issue Orchestration), `R-PDD-EXEC-002` (Role-Separated Prompt Chaining).
* **Exposure:**
  * **CLI:** ✅ (Background daemon execution)
  * **TUI:** ❌ None
  * **GUI:** ❌ None

### 1.3. Router / Gateway (PDD Enforcement Layer)
*File: `router/main.py`*
* **Features:**
  * Dynamic Backend Selection (`split`, `ollama`, `p40` based on model tags).
  * Real-time PDD Rule Injection (prepends Postgres rules to system prompts).
  * Cryptographic Prompt Hashing (`prompt_hash`) for audit immutability.
  * Audit Logging to Postgres (`agent_audit` table).
  * Dashboard API serving.
* **Governing Rules:** `R-PDD-GOV-001` (Single Source of Truth), `R-PDD-AUDIT-001` (Computational Audit Trails).
* **Exposure:**
  * **GUI:** ✅ (Audit logs viewable on Dashboard; Port/Timeouts viewable in Settings)
  * **CLI:** ✅ (`01_start_router.sh`)
  * **TUI:** ❌ None

### 1.4. Ollama Controller & VGPU Manager
*Files: `scripts/ollama_controller.py`, `scripts/vgpu_manager.py`*
* **Features:**
  * REST API / SDK model switching, pulling, loading, and offloading.
  * Live VRAM calculating and dynamic context-window truncation.
  * Hardware mapping (P40 vs 3070 routing).
* **Governing Rules:** `R-HW-GPU-001` (P40 Thermal Limit), `R-HW-GPU-002` (Display GPU Assignment), `PDD-VRAM-001` (Dynamic VRAM rules).
* **Exposure:**
  * **GUI:** ⚠️ Partial (Default model selectable in Settings; No live VRAM charts)
  * **CLI:** ✅ (Self-test suite)
  * **TUI:** ❌ None

### 1.5. Stitch Bus & Valkey
*Files: `scripts/stitch.py`, `valkey_local.conf`*
* **Features:**
  * Redis-backed Pub/Sub for inter-agent communication.
  * `send_task` and `get_task` envelope framing.
* **Governing Rules:** `PDD-CACHE-001` (Caching), `R-PDD-EXEC-001` (Prompts as Versioned Artifacts).
* **Exposure:**
  * **GUI:** ❌ None
  * **CLI:** ✅ (Background processes)
  * **TUI:** ❌ None

---

## 2. Extensions & Custom Features

### 2.1. Governor & Behavior Monitor
*Files: `scripts/governor.py`, `scripts/behavior_monitor.py`*
* **Features:**
  * Scans agent outputs for behavioral drift.
  * Automatically formats and inserts `pdd_proposals` into Postgres for human review.
* **Governing Rules:** `R-PDD-AUDIT-002` (Governance Metrics), `R-PDD-AUDIT-003` (Intervention Controls).
* **Exposure:**
  * **GUI:** ✅ (Proposals table on Dashboard)
  * **CLI:** ✅ (Background loop)
  * **TUI:** ❌ None

### 2.2. Knowledge Graph (KG) & Pruner
*Files: `scripts/knowledge_graph.py`, `scripts/kg_pruner.py`*
* **Features:**
  * Extracts JSON nodes/edges from codebase semantics and conversations.
  * Auto-prunes stale or orphaned nodes to prevent context bloat.
* **Governing Rules:** `R-PDD-KG-001` (Knowledge Graph Maintenance).
* **Exposure:**
  * **GUI:** ⚠️ Minimal (Only shows raw Node/Edge count on Dashboard)
  * **CLI:** ✅ (Background loop)
  * **TUI:** ❌ None

### 2.3. Workspace Security Scanner
*File: `scripts/workspace_sec_scan.py`*
* **Features:**
  * Deep scans the `workspaces/` directory for vulnerabilities or leaked secrets.
* **Governing Rules:** `R-PDD-SEC-001` (Workspace Security Scanning).
* **Exposure:**
  * **CLI:** ✅
  * **GUI / TUI:** ❌ Nowhere

### 2.4. AST Indexer & Smart Fetch
*Files: `scripts/ast_indexer.py`, `scripts/smart_fetch.py`, `scripts/search_context.py`*
* **Features:**
  * Parses Python code into Abstract Syntax Trees for semantic search.
  * Retrieves exact function signatures for agent context augmentation.
* **Governing Rules:** `R-PDD-MD-001` (Prompts Select Intent), `R-PDD-MD-002` (Structure of Authoritative Markdown).
* **Exposure:**
  * **CLI:** ✅ (Background tool)
  * **GUI / TUI:** ❌ Nowhere

### 2.5. Git Worker & Metadata
*Files: `scripts/git_worker.sh`, `scripts/git_metadata.py`*
* **Features:**
  * Auto-commits agent-generated changes with formatted metadata.
* **Governing Rules:** `R-PDD-GIT-001` (Automated Version Control).
* **Exposure:**
  * **CLI:** ✅
  * **GUI / TUI:** ❌ Nowhere

### 2.6. Atlas Bridge
*File: `scripts/atlas_bridge.py`*
* **Features:**
  * Connects AXiomEngine to external data/APIs.
* **Governing Rules:** `R-PDD-ATLAS-001` (AI Atlas Code Engineering).
* **Exposure:**
  * **CLI:** ✅
  * **GUI / TUI:** ❌ Nowhere

### 2.8. Plannotator Integration
*Files: `extensions/plannotator_ext.py`, `pi/pi.py`, `router/main.py`, `/home/cane/.local/bin/plannotator`*
* **Features:**
  * Visual Plan Annotation (Delete, Insert, Replace, Comment).
  * Visual Code Review (Diff line-by-line feedback).
  * Encrypted Sharing (AES-256-GCM E2E encryption for shared plan links).
  * Lifecycle Hooks (Intercepts `plan_created` events for HITL verification).
* **Governing Rules:** `R-PDD-GOV-005` (Visual Feedback Loop), `R-PDD-SEC-004` (Data Exfiltration Prevention).
* **Exposure:**
  * **CLI:** ✅ (`/plannotator-review`, `/plannotator-annotate`, `/plannotator-last` in `pi`)
  * **TUI:** ✅ (Integrated into `pi` shell; triggers visual overlay in browser)
  * **GUI:** ✅ (Dedicated "Visual Review" card and "Launch Review" button on Dashboard)

### 2.9. TUI (Terminal User Interface)
*File: `scripts/rich_tui.py`*
* **Features:**
  * Provides a styled command-line chat application.
  * Integrated Plannotator triggers via slash commands.
* **Governing Rules:** `R-PDD-GOV-003` (Interface Standardization).
* **Exposure:**
  * **TUI:** ✅ (It is the TUI itself. No hardware management, no routing config, no fleet management exposed inside it).

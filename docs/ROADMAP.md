# Agentic OS Architecture Plan
## Ubuntu 26.04 LTS · ROG B650E-F · RTX 3070 + Tesla P40 + AMD Raphael

> **Governed by PDD** — All decisions below are authoritative artifacts per `R-PDD-GOV-001`.  
> **Isolation Protocol:** All AXiomEngine operations are restricted to the `/mnt/usb.../Projects/axiomengine` directory.

---

## 🛠 Phase 0 — Core AI Stack (COMPLETED)
- [x] **Postgres 18 & pgvector**: Initialized on port 5433 with `io_uring` tuning.
- [x] **Valkey**: Key-value store and message broker on port 6379.
- [x] **Inference Infrastructure**: Nemotron (P40+3070 split) and Ollama (Qwen 3.6).
- [x] **Thermal Safety**: GPU thermal monitor service active (85°C limit).
- [x] **Router Gateway**: Governed FastAPI router live on port 9001.

---

## 🤖 Phase 1 — Agentic Tier (COMPLETED)
- [x] **Archon (Architect)**: System-level planning agent deployed.
- [x] **Pi (Personal Intelligence)**: User-facing assistant agent deployed.
- [x] **PDD Governance**: 19 authoritative rules ingested into Postgres vector store.
- [x] **Master Entry Point**: `AGENTS.md` established as the single starting pointer.

---

## 🧬 Phase 2 — Context Assembly & Automation (IN PROGRESS)
- [x] **Semantic Indexing**: Index local files in `/Projects` into Postgres. (Implemented via `02_index_context.py`).
- [x] **n8n Workflow Automation**: Deploy Docker-based n8n. (Fix: `sudo snap connect docker:removable-media`).
- [x] **Stitch Messaging**: Initialize inter-agent communication via Valkey. (Implemented via `stitch.py`).
- [x] **Archon Workflows**: Implement the first automated code-review and safety pipelines. (Implemented via `workflow_review.py`).

---

## ⚖️ Phase 3 — PDD Governance Reinforcement (IN PROGRESS)
- [x] **Durable Rule Enforcement**: Hard-coding rule checks into agent loop-backs. (Implemented via `governor.py`).
- [x] **Audit Dashboard**: Web-based view of the `agent_audit` table and drift detection. (Implemented at `/admin/dashboard`).
- [x] **Intent Mapping**: Automating the link between Markdown intent and generated code. (Implemented via `intent_mapper.py`).

---

## 🧠 Phase 3.5 — Personal Intelligence (PI) Augmentation (IN PROGRESS)
- [x] **Always-On Heartbeat**: Pi proactively monitors tasks and system state. (Implemented via `03_heartbeat.py`).
- [x] **Web Fetcher**: Agents can read and extract clean markdown from URLs. (Implemented via `smart_fetch.py`).
- [x] **TOON Encoding**: Token-efficient object notation for prompt compression. (Implemented via `toon.py`).
- [x] **SIS Learning Loop**: Automatic lesson extraction from audit results. (Implemented via `sis_loop.py`).

---

## 🛡️ Phase 4 — Sandboxing & Safety
- [x] **MicroVM Sandboxing**: Using `qemu-microvm` to run agent-generated scripts safely. (Verified: `vmlinux` and `rootfs.ext4` active).
- [x] **Resource Capping**: CGroups for limiting agent CPU/RAM usage. (Implemented via `sandbox.py`).
- [ ] **VGPU Partitioning**: (Optional) Isolated VRAM slices for concurrent agents.

---

## 🔌 Phase 5 — Agentic Ecosystem Extensions (IN PROGRESS)
- [x] **Dispatcher & Subagents**: Intelligent task routing (`dispatcher.py`, `git_worker.sh`).
- [x] **Behavior Monitors**: Continuous PDD drift auditing (`behavior_monitor.py`).
- [x] **Interactive TUI & Forms**: Rich display and user prompts (`rich_tui.py`, `user_prompt.py`).
- [x] **Security & Credentials**: Approval gates and secure vaults (`uac.py`, `keychain.py`).
- [x] **Advanced Knowledge**: Graph databases, AST indexing, and wiki generation (`knowledge_graph.py`, `ast_indexer.py`, `wiki_manager.py`).
- [x] **I/O Context**: Web fetching and git state injection (`smart_fetch.py`, `git_metadata.py`).
- [x] **Remote Access**: Settings registry and remote gateways (`settings_registry.py`, `remote_gateway.py`).
---

## 🧬 Phase 6 — Swarm Orchestration & Advanced Governance (INITIATED)
- [x] **Swarm Coordinator**: Hierarchical task breakdown and multi-agent dispatch (`swarm_coordinator.py`).
- [x] **VGPU Logical Partitioning**: VRAM reservation system to prevent OOM (`vgpu_manager.py`).
- [x] **Hybrid Sandboxing**: Support for MicroVM execution in the sandbox layer (`sandbox.py`).
- [x] **Swarm Governance**: Authoritative rules for delegation and recursion control (`R-PDD-SWARM-001`).
- [x] **Global State Sync**: CRDT-based shared context across distributed agents (`sync_state.py`).
- [x] **Collaborative Refinement**: Sub-agents can propose rule mutations for review (`propose_rule.py`, `pdd_proposals` table).
- [x] **Atlas Code Engineering**: Integrated `@wizdear/atlas-code` multi-agent orchestration for end-to-end feature dev.
- [x] **Symphony Service**: SPEC.md compliant autonomous issue orchestrator (`symphony.py`).

---

## 🧠 Phase 7 — Cognitive Evolution & Deep Governance (PLANNED)
- [x] **Non-Blocking Governance Check**: Pre-check prompts against governance without blocking; propose new rules or separate branches for non-compliant changes. (Implemented via `nonblocking_governor.py`, `pdd_proposals` table added to install script.)
- [x] **Governed Skill Harvesting**: Automatically codify successful workflows into "Skills" that must strictly adhere to PDD mandates (no auto-approval). (Implemented via `skill_harvester.py`; drafts are Governor-checked and staged to `.pi/skills_pending/`, promoted only by explicit `--approve`.)
- [x] **User Intelligence (The Interview)**: Implement an "Interview" phase to capture self-declared job roles, expectations, and company-specific lingo. (Implemented via `user_interview.py` + `user_profile` table; surfaced through `search_context.py`.)
- [x] **Persistent Conversational Memory**: Add long-term session recall via semantic search or FTS5 (addressing assistant amnesia). (Implemented via `conversation_memory.py` + `conversation_memory` table with pgvector + tsvector fallback; router persists each turn best-effort, `search_context.py` recalls relevant prior turns.)
- [x] **PI Rule Extensions**: Index and inject specific rule behaviors through specialized PI extensions. (Implemented via `ExtensionAPI.registerRuleProvider` + `index_extension_rules.py`, which embeds extension-contributed rules into `pdd_rules` so they flow through the existing injection pipeline; see `extensions/gpu_thermal_rules.py` for an example.)
- [x] **The Governance Manifest Template**: Standardize the AXiomEngine audit results into a reusable template for other ecosystems. (Implemented via `docs/contracts/governance_manifest_template_contract.md` + `scripts/governance_manifest_template.py`, which aggregates release/integrity/hardware/mission artifacts into one ecosystem-agnostic manifest.)
- [ ] **Remote Compute (Long-term)**: Consider off-host execution via Modal or SSH sandboxes. (Scoped, not implemented — see `docs/roadmap/REMOTE_COMPUTE_SCOPING.md`: recommends prototyping an SSH sandbox `AgentSandbox` mode first, with audit-sink-reachability as a hard precondition, before generalizing to a Modal backend.)

---

## Hardware Allocation (Authoritative)
| Resource | AI Role | Gaming Role |
|---|---|---|
| **RTX 3070 8GB** | LLM Head / VAE | Primary Render |
| **Tesla P40 24GB** | LLM Body / UNet | Shader Cache |
| **AMD Raphael** | Display Adapter | Idle |
| **96GB DDR5** | Context Overflow | OS / Game RAM |
| **60TB USB Hub** | Vector Store / Models | Asset Storage |

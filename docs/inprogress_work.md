# In-Progress Work: Governance Trifecta Swarm Audit

> [!IMPORTANT]
> **SYSTEM STATUS: SPIN-DOWN / GPU RECOVERY**
> The mission is currently paused due to GPU instability. Work is scheduled to resume once the RTX 3070 and Primary GPU have been reconfigured and verified.

## 🛠️ Post-GPU Repair Verification Checklist
Perform these checks before resuming the 33,196-instance mission:

- [ ] **BIOS/iGPU Check**: Confirm AMD iGPU is handling primary display (Gnome/X11).
- [ ] **NVIDIA Isolation**: `nvidia-smi` must show **0MiB** on GPU 0 (RTX 3070).
- [x] **Ollama Recovery**: `ollama serve` must be restarted and verified. Managed lanes are active on `11436` (RTX 3070) and `11437` (P40), with default fallback on `11434`.
- [x] **Model Hot-Swap**: Verify `qwen3.6:27b` and `gemma4:e2b` are responsive via the Router/Ollama lanes. Current local check: `gemma4:e2b` and `cmdmbox/skill-expert` respond on `11436`; `qwen3.6:27b` responds on `11437`. `gemma4:e4b` is not assigned to RTX 3070 because its ~9GB footprint exceeds the 8GB card.

## 🐝 Swarm Configuration (Model Routing)
The `DataCatalogFactory.py` mission is optimized for dual-GPU orchestration:

| Agent Role | Model | Hardware Target | Task Description |
| :--- | :--- | :--- | :--- |
| **Researcher** | `gemma4:e2b` | **RTX 3070** | General high-volume extraction: keywords, summaries, taxonomy, classification, and pre-digests. This is the RTX-safe Gemma4 lane (~7.2GB for an 8GB card). |
| **Skill Specialist** | `cmdmbox/skill-expert` | **RTX 3070** | Specialized Gemma4-derived lane for creating/refining agent skills, skill triggers, and skill validation checklists. |
| **Architect** | `qwen3.6:27b` | **Primary GPU** | Synthesize technical dissertations and deep governance reasoning. |
| **Auditor** | Programmatic | **CPU** | Regex, Grep, and AST structural indexing. |

## 📅 Mission Tasks & Milestones

### 1. Swarm Orchestration Stabilizing
- [x] Integrate `scripts/pi_ai.py` into the swarm controller.
- [x] Implement dynamic model routing (Gemma-4 vs Qwen-27B).
- [x] Fix `DataCatalogFactory.py` to explicitly pass model parameters to `local_ai_inference`.
- [x] Record RTX 3070 model routing: use `gemma4:e2b` for general Researcher work and reserve `cmdmbox/skill-expert` for skill-authoring tasks only.

### 2. 33,196-Instance Audit Execution
- [x] Initial rule discovery (11,407 rules).
- [x] Instance mapping (33,196 targets).
- [ ] **[IN-PROGRESS]** High-concurrency audit pass (Target: 100% hardware utilization).
- [ ] Metadata fusion into `COMPLETE_GOVERNANCE_DATASET.json`.

### 3. Interface Integration
- [x] CLI (`pi`) support for governance querying.
- [x] TUI (`pi_tui.py`) live mission monitoring.
- [ ] **[TODO]** Wire mission progress bar to the Dashboard GUI.

### 4. User Modeling & Cognitive Evolution (Queued)
- [ ] **Phase 1: The Interview**: Develop a script to interview the user for job roles and expectations.
- [ ] **Phase 2: Lingo Ingestion**: Index company-specific lingo and descriptions into the Knowledge Graph.
- [ ] **Phase 3: Conversational Memory**: Integrate semantic search for long-term session recall.
- [ ] **Phase 4: PI Rule Extensions**: Index PI rule behaviors for dynamic injection.

---
*Status: Ready for Swarm Launch / Cognitive Queue Initialized*

# AXiomEngine Context Entry Point
# ════════════════════════════════════════════════════════════════════════════
// RULE-START: RULE-START
// RULE-START: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-END: RULE-START
// RULE-START: R-PDD-CORE-003
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-GOV-001
# R-PDD-CORE-003: This is the SINGLE AUTHORITATIVE STARTING POINTER.
// RULE-END: R-PDD-GOV-001
// RULE-END: R-PDD-CORE-003
// RULE-START: R-PDD-GOV-001
# Every agent must read this file before executing any task.
// RULE-END: R-PDD-GOV-001
# Folder location does NOT confer authority — this declaration does.
// RULE-START: R-PDD-GOV-001
# ════════════════════════════════════════════════════════════════════════════
// RULE-END: R-PDD-GOV-001

## Identity
// RULE-START: R-PDD-CORE-001
- **System:** AXiomEngine on Ubuntu 26.04 LTS
// RULE-END: R-PDD-CORE-001
// RULE-START: R-PDD-GOV-001
// RULE-START: R-PDD-CORE-001
// RULE-START: R-PDD-CORE-002
// RULE-START: R-PDD-GOV-001
// RULE-END: R-PDD-CORE-002
// RULE-END: R-PDD-CORE-001
// RULE-END: R-PDD-GOV-001
// RULE-START: R-PDD-CORE-001
- **Hardware:** ASUS ROG B650E-F | RTX 3070 8GB | Tesla P40 24GB | 96GB DDR5
// RULE-END: R-PDD-CORE-001
// RULE-START: R-PDD-CORE-002
// RULE-START: R-PDD-CORE-002
// RULE-END: R-PDD-CORE-002
// RULE-END: R-PDD-GOV-001
// RULE-END: R-PDD-CORE-002
// RULE-START: R-PDD-CORE-001
- **Router:** http://127.0.0.1:9001  (OpenAI-compatible endpoint)
// RULE-END: R-PDD-CORE-001
// RULE-START: R-PDD-GOV-001

// RULE-START: R-PDD-CORE-002
// RULE-END: R-PDD-GOV-001
// RULE-END: R-PDD-CORE-002
// RULE-START: R-PDD-CORE-001
// RULE-START: R-PDD-CORE-002
// RULE-START: R-PDD-CORE-001
// RULE-END: R-PDD-CORE-002
// RULE-END: R-PDD-CORE-001
## Active Governing Rules
// RULE-END: R-PDD-CORE-001
// RULE-START: R-PDD-GOV-001
All rules below are AUTHORITATIVE per R-PDD-GOV-001.
// RULE-START: R-PDD-CORE-002
// RULE-END: R-PDD-GOV-001
// RULE-END: R-PDD-CORE-002
Retrieve from Postgres: `SELECT * FROM pdd_rules WHERE active=TRUE ORDER BY rule_id;`
Or read from: `.context/pdd/`
// RULE-START: R-PDD-CORE-001

// RULE-END: R-PDD-CORE-001
// RULE-START: R-PDD-CORE-002
**Critical rules in effect:**
// RULE-END: R-PDD-CORE-002
- `R-PDD-CORE-001` — AI does not infer intent; intent must be explicit
- `R-PDD-CORE-002` — Folder structure is NOT authority
// RULE-START: R-PDD-GOV-002
// RULE-START: R-PDD-AUDIT-001
// RULE-START: R-PDD-EXEC-002
- `R-PDD-GOV-002` — AI agents MUST NOT author or mutate intent documents
// RULE-END: R-PDD-EXEC-002
// RULE-END: R-PDD-AUDIT-001
// RULE-END: R-PDD-GOV-002
- `R-PDD-AUDIT-001` — All sessions logged with prompt ID, model, rules cited
- `R-PDD-EXEC-002` — Role separation: Planning ≠ Execution ≠ Review

## Active Inference Mode
**Current default:** MODE 1 — Split LLM Inference
- Nemotron-3-Nano-30B → P40 (body, 20GB) + RTX 3070 (head, 5.6GB)
- Endpoint: `http://127.0.0.1:8080` (direct) or `http://127.0.0.1:9001` (via router)

See: `.context/modes/mode1_split_llm.md` for full parameters.

## Hardware Constraints
See: `.context/hardware/gpu_allocation.md`

**Critical:** AMD Raphael iGPU handles display in AI modes.
RTX 3070 and P40 are for AI only during Modes 1-3.

## Agentic Tools Available
| Tool | Endpoint / Command | Role |
|---|---|---|
| AXiomEngine Router | http://127.0.0.1:9001 | Central gateway |
| Archon | `python archon/archon.py` | System Architect |
| Pi | `python pi/pi.py` | Personal Intelligence |
| Nemotron snap | http://127.0.0.1:8330 | Split LLM (Mode 1) |
| Ollama (Qwen 3.6) | http://127.0.0.1:11434 | Alt LLM |
| Postgres 18 | localhost:5433 db=axiomengine | State + vectors |
| Valkey | localhost:6379 | Cache + messaging |
| Open-WebUI | (snap) | Chat UI |

## Non-Goals (R-PDD-GOV-002)
- Agents MUST NOT modify files in `.context/pdd/`
// RULE-START: R-PDD-EXEC-001
// RULE-START: R-PDD-EXEC-001
// RULE-END: R-PDD-EXEC-001
- Agents MUST NOT modify `AGENTS.md`
// RULE-END: R-PDD-EXEC-001
- Agents MUST NOT skip audit logging
- Agents MUST NOT run without citing at least one governing rule

## Session Start Checklist (R-PDD-EXEC-001)
Before any agent executes a task:
1. ✅ Read this file
2. ✅ Identify applicable rules from `.context/pdd/`
3. ✅ Cite rule IDs in session metadata
4. ✅ Confirm active mode is correct for task
5. ✅ Log session to agent_audit via router

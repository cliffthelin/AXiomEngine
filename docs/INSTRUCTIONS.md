# AXiomEngine General Instructions & Mission Parameters

This document serves as the **Sovereign Mandate** for the AXiomEngine ecosystem. It defines the architecture, governance layers, and autonomous roles that ensure all system actions are audit-defensible and intent-aligned.

---

## 🏛️ The Sovereign Mandate: 13-Layer Intent Resolution
AXiomEngine operates on an axiomatic 13-layer model where "Context-as-Code" is the primary authority. All system evolution must pass through the **Intent Stack**:

1.  **L13: Process Records** (Provenance - Hermes)
2.  **L10-L12: Metadata & Dependencies** (Graph)
3.  **L8: DataConcepts** (Governance Anchors)
4.  **L6: Decisions** (Sovereign Determinations)
5.  **L3: PDD Rules** (Static Axioms)
6.  **L2: SDD** (Architecture/Extraction)
7.  **L1: Code Reality** (Implemented Logic)

---

## 🛰️ Autonomous Roles & Responsibilities

| Role | Designation | Primary Mandate |
|:---|:---|:---|
| **Archon** | Harness Maker | **Creation & Execution**. Builds autonomous harnesses to satisfy intent. Monitors L1 vs L3. |
| **Hermes** | Scribe & Recall | **Determination & Memory**. Records L6 Decisions and L13 Process Records. Performs Cohesiveness Audits. |
| **Reversa** | Archaeologist | **Extraction**. Translates legacy code (L1) into intent-aligned blueprints (L2/L3). |
| **Discovery** | Prospector | **Detection**. Scans reality for new candidate rules and governance anchors (L8). |

---

## 🛡️ The Sovereignty Protocol (HITL)
AXiomEngine enforces a strict **Candidate Layer** to ensure human sovereignty over the laws of the system:
1.  **Discovery**: Agents propose "Candidates" to `data/candidates/`.
2.  **Review**: Candidates are staged and "Shadowed" to observe impact without enforcement.
3.  **Promotion**: Candidates are formally signed off and promoted to **L6 Decisions** using the `candidate_manager.py`.
4.  **Enforcement**: Once promoted, Archon enforces the decision across the codebase.

---

## 🖥️ Operational Monitoring (The Archon Harness)
Monitoring is **Policy-Driven**, not ad-hoc:
- **Watchdog**: The `archon_harness.py` enforces L3 monitoring policies (defined in `data/archon_policies.json`).
- **Self-Correction**: The harness automatically troubleshoots stalls, restarts services (Ollama/Valkey), and relaunchs missions.
- **Auditability**: Every autonomous intervention must generate an **L13 Process Record**.

---

## 🛠️ Infrastructure Rationale
- **Inference**: Local-first via **Ollama** (P40 for Heavy 27B+ reasoning, 3070 for Light/Offload).
- **Isolation**: **Docker** for cellular environment isolation.
- **State**: **Valkey** for high-speed synchronous state and queue management.
- **Methodology**: **Reversa** (Extraction) + **PDD** (Axiomatic Governance).

---
*Built for Learning. Governed for Sovereignty.*

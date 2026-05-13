# Governance Dashboard Layer Contract (v1.3.1)

This document defines the authoritative mapping rules between promoted determinations (`DEC-XXXX`) and the 13 Sovereign Layers of AXiomEngine.

## The 13 Sovereign Layers

| ID | Layer Name | Activation Rule | Confidence |
| :--- | :--- | :--- | :--- |
| 01 | Identity & Intent | `decision_type: "IntentValidation"` OR top-level `closer_version` present | Governed |
| 02 | Scope & Boundary | `decision_type: "ScopeValidation"` OR top-level `closer_version` present | Governed |
| 03 | Capability & Skill | `decision_type: "SkillDetermination"` | Governed |
| 04 | Resource & Hardware | `decision_type: "HardwarePolicy"` | Governed |
| 05 | Security & Trust | `decision_type: "SecurityDetermination"` | Governed |
| 06 | Decision & Policy | `decision_type: "PolicyDefinition"` | Governed |
| 07 | Observation & Evidence | `evidence_context.evidence_snapshots` length > 0 | Governed |
| 08 | Analysis & Rationale | `statement` length > 10 AND `reviewed_at` present | Governed |
| 09 | Memory & Context | `prompted_by.context_type` matches "mission_audit" | Governed |
| 10 | Communication & Protocol | `decision_type: "ProtocolValidation"` | Governed |
| 11 | Action & Execution | `decision_type: "ExecutionPolicy"` | Governed |
| 12 | Verification & Audit | `prompted_by.mission_pack_id` present | Governed |
| 13 | Evolution & Meta | `decision_type: "GovernancePolicy"` | Governed |

## Activation Types
- **Direct**: Based on explicit `decision_type`.
- **Inferred**: Based on provenance metadata (e.g., `closer_version` implies scope/intent was governed).
- **Provisional**: Based on existence of required fields (e.g., evidence presence).

## Visual States
- **GOVERNED**: Rule matches at least one promoted determination.
- **UNMAPPED**: No matching determination found in the registry.

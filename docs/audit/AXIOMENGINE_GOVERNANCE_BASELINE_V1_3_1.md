# AXiomEngine Governance Baseline v1.3.1 (Audit-Frozen)

## 1. Executive Summary
AXiomEngine Governance Baseline v1.3.1 is now **frozen for official audit**. This baseline establishes a stable, forensic-ready infrastructure for autonomous candidate discovery, sovereign human review, and hardened determination promotion.

### The Governance Loop
- **Discovery**: `harness_manager.py` (v1.2.1) identifies candidate findings across multi-shard audits.
- **Review**: `harness_builder_prototype.html` provides the sovereign cockpit for human governorship.
- **Promotion**: `governance_closer.py` (v1.3.1) validates and promotes accepted findings into the authoritative registry.
- **Registry**: `data/decisions.json` stores hash-linked determinations with durable evidence snapshots.
- **Visualization**: `governance_dashboard.html` (v1.3.1) provides a read-only health monitor grounded in real mission artifacts.

---

## 2. Frozen Components
The following components constitute the authoritative v1.3.1 baseline:

- **scripts/governance_closer.py**: Hardened promotion node.
- **governance_dashboard.html**: Authoritative health visualizer.
- **scripts/harness_manager.py**: Multi-shard mission orchestrator.
- **harness_builder_prototype.html**: Sovereign review interface.
- **data/decisions.json**: Authoritative decision registry.
- **docs/contracts/closer_report_contract.md**: Standardized mission accounting schema.
- **docs/contracts/promoted_decision_contract.md**: Standardized determination schema.
- **docs/contracts/governance_dashboard_layer_contract.md**: Standardized 13-layer mapping rules.
- **tests/test_governance_closer.py**: Operational safety tests.
- **tests/test_governance_closer_contract.py**: Schema and contract compliance tests.
- **tests/test_governance_dashboard_logic.py**: Dashboard classification and layer mapping tests.

---

## 3. Contract Registry

### Closer Report Contract
- **Artifact Governed**: `closer_report.json`
- **Required Fields**: `closer_version`, `timestamp`, `mission_pack_id`, `valid_promotion_count`, `rejected_count`, `validation_errors`.
- **Downstream Consumer**: Governance Dashboard.
- **Audit Purpose**: Ensures total mission accounting and historical attempt preservation.

### Promoted Decision Contract
- **Artifact Governed**: Individual records in `data/decisions.json`.
- **Required Fields**: `decision_id`, `decision_type`, `promotion_policy`, `evidence_context`, `closer_version`.
- **Downstream Consumer**: Hermes Integration / Compliance Monitors.
- **Audit Purpose**: Ensures determinations are self-contained and forensically verifiable.

### Governance Dashboard Layer Contract
- **Artifact Governed**: `governance_dashboard.html` visualization.
- **Required Fields**: Mapping rules for all 13 Sovereign Layers.
- **Downstream Consumer**: Human Stakeholders / Auditors.
- **Audit Purpose**: Ensures "GOVERNED" status is backed by explicit determination metadata.

---

## 4. Test Evidence
**Command Executed**:
`PYTHONPATH=. python3 tests/test_governance_closer.py && PYTHONPATH=. python3 tests/test_governance_closer_contract.py && PYTHONPATH=. python3 tests/test_governance_dashboard_logic.py`

**Results**:
- **Status**: 14/14 Tests Passing.
- **Scope**: operational safety, schema compliance, artifact classification, layer mapping, and idempotency.
- **Exclusions**: Full project-wide application tests (e.g., individual worker logic) are outside this governance-stack baseline.

---

## 5. Official Known Limitations
- Dashboard currently uses manual browser-based artifact import.
- Dashboard is read-only; no mutation operations are supported from the UI.
- Layer saturation is strictly dependent on promoted determination metadata; unmapped decisions will not activate layers.
- Static HTML dashboard does not yet auto-discover project files on the local filesystem.

---

## 6. Governance Invariants
- **Evidence-First**: No accepted finding may be promoted without traceable evidence and hash-linking.
- **Strict-Abort**: Strict mode MUST abort on any validation or traceability failure.
- **Audit-Preservation**: Historical closer reports MUST be preserved under `closer_reports/`.
- **Separation of Concerns**: The dashboard MUST NOT mutate governance artifacts.
- **No Ambiguity**: `global_decisions.json` (review export) MUST NEVER be treated as `data/decisions.json` (authoritative registry).

---

## 7. Audit Decision
- **Baseline Status**: **FROZEN**
- **Governance Maturity**: Review-grade / Forensic-ready.
- **Next Phase**: v1.4.0 Project Integration.

---

## 8. Future Evolution Path (Backlog)
- [ ] v1.4.0: Local project auto-discovery server (Automated Dashboard loading).
- [ ] v1.4.0: Dashboard artifact manifest loader.
- [ ] v1.4.0: Governance CLI command group (`axiomengine gov ...`).
- [ ] v1.4.0: Full test suite integration (CI/CD alignment).
- [ ] v1.4.0: Signed baseline manifest (GPG/PGP).

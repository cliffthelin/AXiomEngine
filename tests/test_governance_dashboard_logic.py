import unittest
import json

# Dashboard Logic Port for Verification (V1.3.1)
class DashboardLogic:
    @staticmethod
    def isCloserReport(j):
        return bool(j.get("closer_version") and "promoted_decision_ids" in j and "validation_errors" in j)
    
    @staticmethod
    def isPromotedDecisionRegistry(j):
        decs = j.get("decisions")
        return isinstance(decs, list) and (len(decs) == 0 or "decision_id" in decs[0])
    
    @staticmethod
    def isGlobalReviewExport(j):
        decs = j.get("decisions")
        return decs and not isinstance(decs, list) and "mission_pack_id" in j
    
    @staticmethod
    def isGlobalMissionReport(j):
        return bool(j.get("mission_pack_id") and j.get("manager_run_id") and j.get("pack_hash") and not j.get("closer_version"))

    @staticmethod
    def getMissionStatus(r):
        if not r: return "MISSING_REPORT"
        if r.get("dry_run"): return "DRY_RUN"
        if len(r.get("validation_errors", [])) > 0 and r.get("strict"): return "STRICT_ABORT"
        if r.get("rejected_count", 0) > 0: return "PARTIAL_SUCCESS"
        return "SUCCESS"

    @staticmethod
    def getActiveLayers(decisions):
        active = set()
        for d in decisions:
            # v1.3.1 Contract Rules
            if d.get("decision_type") == "IntentValidation" or d.get("closer_version"): active.add(0)
            if d.get("decision_type") == "ScopeValidation" or d.get("closer_version"): active.add(1)
            if d.get("decision_type") == "SkillDetermination": active.add(2)
            if d.get("decision_type") == "HardwarePolicy": active.add(3)
            if d.get("decision_type") == "SecurityDetermination": active.add(4)
            if d.get("decision_type") == "PolicyDefinition": active.add(5)
            if len(d.get("evidence_context", {}).get("evidence_snapshots", [])) > 0: active.add(6)
            if len(d.get("statement", "")) > 10 and d.get("reviewed_at"): active.add(7)
            if d.get("prompted_by", {}).get("context_type") == "mission_audit": active.add(8)
            if d.get("decision_type") == "ProtocolValidation": active.add(9)
            if d.get("decision_type") == "ExecutionPolicy": active.add(10)
            if d.get("prompted_by", {}).get("mission_pack_id"): active.add(11)
            if d.get("decision_type") == "GovernancePolicy": active.add(12)
        return active

class TestDashboardLogic(unittest.TestCase):
    def test_artifact_classification(self):
        # 1. Closer Report
        report = {"closer_version": "1.3.1", "promoted_decision_ids": [], "validation_errors": []}
        self.assertTrue(DashboardLogic.isCloserReport(report))
        
        # 2. Promoted Registry (data/decisions.json)
        registry = {"decisions": [{"decision_id": "DEC-1", "statement": "valid"}]}
        self.assertTrue(DashboardLogic.isPromotedDecisionRegistry(registry))
        self.assertFalse(DashboardLogic.isGlobalReviewExport(registry))
        
        # 3. Global Review Export (global_decisions.json)
        export = {"mission_pack_id": "MPK-1", "decisions": {"FND-1": "ACCEPTED"}}
        self.assertTrue(DashboardLogic.isGlobalReviewExport(export))
        self.assertFalse(DashboardLogic.isPromotedDecisionRegistry(export))
        
        # 4. Global Mission Report
        g_report = {"mission_pack_id": "MPK-1", "manager_run_id": "MGR-1", "pack_hash": "H1"}
        self.assertTrue(DashboardLogic.isGlobalMissionReport(g_report))

    def test_mission_status_resolution(self):
        # Strict Abort
        abort = {"strict": True, "validation_errors": ["Missing finding"], "dry_run": False}
        self.assertEqual(DashboardLogic.getMissionStatus(abort), "STRICT_ABORT")
        
        # Dry Run
        dry = {"dry_run": True, "validation_errors": []}
        self.assertEqual(DashboardLogic.getMissionStatus(dry), "DRY_RUN")
        
        # Partial Success
        partial = {"strict": False, "rejected_count": 1, "validation_errors": ["Error"]}
        self.assertEqual(DashboardLogic.getMissionStatus(partial), "PARTIAL_SUCCESS")

    def test_layer_activation_contract(self):
        # Security Determination activates Layer 4 (Security & Trust)
        decs = [{"decision_type": "SecurityDetermination"}]
        self.assertIn(4, DashboardLogic.getActiveLayers(decs))
        
        # Closer-backed decision activates Layer 0 & 1 (Intent & Scope)
        decs = [{"closer_version": "1.3.1"}]
        self.assertIn(0, DashboardLogic.getActiveLayers(decs))
        self.assertIn(1, DashboardLogic.getActiveLayers(decs))
        
        # Audit metadata activates Layer 11 (Verification & Audit)
        decs = [{"prompted_by": {"mission_pack_id": "MPK-1"}}]
        self.assertIn(11, DashboardLogic.getActiveLayers(decs))

if __name__ == "__main__":
    unittest.main()

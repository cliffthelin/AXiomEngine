import unittest
import re
from pathlib import Path

class TestGovernanceDashboardApiAdapter(unittest.TestCase):
    def setUp(self):
        self.dashboard_path = Path("governance_dashboard_v1_4.html")
        self.content = self.dashboard_path.read_text()

    def test_additive_integrity(self):
        # Ensure we didn't touch the frozen v1.3.1 dashboard
        frozen_path = Path("governance_dashboard.html")
        self.assertTrue(frozen_path.exists())
        # The new one should be different
        self.assertNotEqual(self.content, frozen_path.read_text())

    def test_api_base_url(self):
        # Must point to the default local discovery server
        self.assertIn('const API_BASE = "http://127.0.0.1:8765";', self.content)

    def test_no_mock_data(self):
        # Should not contain fabricated counts
        self.assertNotIn("33196", self.content)
        self.assertNotIn("33,196", self.content)

    def test_required_endpoints_consumed(self):
        endpoints = [
            "/health",
            "/api/governance/summary",
            "/api/governance/baseline/status",
            "/api/governance/decisions",
            "/api/governance/latest-report",
            "/api/governance/historical-reports",
            "/api/governance/mission-artifacts",
            "/api/governance/manifest"
        ]
        for ep in endpoints:
            self.assertIn(ep, self.content)

    def test_no_mutation_calls(self):
        methods = ["POST", "PUT", "PATCH", "DELETE"]
        for m in methods:
            self.assertNotIn(f"method: '{m}'", self.content)
            self.assertNotIn(f'method: "{m}"', self.content)

    def test_connection_states(self):
        self.assertIn("CONNECTED", self.content)
        self.assertIn("DISCONNECTED", self.content)
        self.assertIn("SERVER_ERROR", self.content)
        self.assertIn("DRIFT DETECTED", self.content)

    def test_resilient_fetch_logic(self):
        # Verify separate required/optional logic exists
        self.assertIn("fetchRequired", self.content)
        self.assertIn("fetchOptional", self.content)
        self.assertIn("NO_REPORT_YET", self.content)

    def test_report_metrics_panel(self):
        # Verify the new metrics display panel
        self.assertIn("Latest Governance Report", self.content)
        self.assertIn("report-status", self.content)
        self.assertIn("report-meta", self.content)

    def test_baseline_manifest_meta(self):
        # Verify consumption of manifest metadata
        self.assertIn("baseline-meta", self.content)
        self.assertIn("created_at", self.content)
        self.assertIn("files?.length", self.content)

if __name__ == "__main__":
    unittest.main()

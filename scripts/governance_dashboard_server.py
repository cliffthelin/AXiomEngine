#!/usr/bin/env python3
"""
AXiomEngine Governance Dashboard Server (v1.4.0 Additive)
=====================================================
Read-only discovery backend for the Governance Dashboard.
Provides a secure API for frozen v1.3.1 artifacts and mission logs.
"""
import json
import argparse
import os
import sys
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from scripts.governance_manifest_verifier import build_manifest_verification_result

VERSION = "1.4.0"

# --- SHARED HELPERS (Module Level) ---

def safe_read_json(path):
    """Safely read and parse JSON, returning error object if malformed."""
    if not path.exists():
        return {"error": "File not found", "path": str(path.name)}
    try:
        return json.loads(path.read_text())
    except Exception as e:
        return {"error": "Malformed JSON", "parse_error": str(e), "path": str(path.name)}

def get_all_reports_from_dirs(mission_dirs):
    """Programmatic discovery of governance reports across directories."""
    reports = []
    for d in mission_dirs:
        # Latest in mission dir
        latest = d / "closer_report.json"
        if latest.exists():
            reports.append(safe_read_json(latest))
        
        # Historical
        hist_dir = d / "closer_reports"
        if hist_dir.exists():
            for f in hist_dir.glob("closer_report_*.json"):
                reports.append(safe_read_json(f))
    
    # Filter out errors and sort by timestamp
    valid_reports = [r for r in reports if isinstance(r, dict) and "error" not in r]
    valid_reports.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return valid_reports

def resolve_mission_status(r):
    """Determine the operational status of a governance mission report."""
    if not r or (isinstance(r, dict) and "error" in r): return "MISSING_REPORT"
    if r.get("dry_run"): return "DRY_RUN"
    if len(r.get("validation_errors", [])) > 0 and r.get("strict"): return "STRICT_ABORT"
    if r.get("rejected_count", 0) > 0: return "PARTIAL_SUCCESS"
    return "SUCCESS"

# --- DISCOVERY HANDLER ---

class GovernanceDiscoveryHandler(BaseHTTPRequestHandler):
    def end_headers(self):
        # Strict Local CORS
        origin = self.headers.get('Origin')
        if origin:
            # Allow localhost, 127.0.0.1, and variants with ports
            pattern = r'^http://(localhost|127\.0\.0\.1)(:\d+)?$'
            if re.match(pattern, origin):
                self.send_header('Access-Control-Allow-Origin', origin)
                self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        routes = {
            "/health": self.handle_health,
            "/api/governance/manifest": self.handle_manifest,
            "/api/governance/baseline/status": self.handle_baseline_status,
            "/api/governance/decisions": self.handle_decisions,
            "/api/governance/latest-report": self.handle_latest_report,
            "/api/governance/historical-reports": self.handle_historical_reports,
            "/api/governance/mission-artifacts": self.handle_mission_artifacts,
            "/api/governance/summary": self.handle_summary
        }

        # Route matching
        handler = routes.get(self.path)
        if handler:
            handler()
        else:
            self.send_error(404, "Route Not Found")

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    # --- ROUTE HANDLERS ---

    def handle_health(self):
        self.send_json({"status": "ok", "version": VERSION, "project_root": str(self.server.project_root)})

    def handle_manifest(self):
        path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        self.serve_file(path)

    def handle_baseline_status(self):
        manifest_path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        status = build_manifest_verification_result(manifest_path, project_root=self.server.project_root)
        self.send_json(status)

    def handle_decisions(self):
        path = self.server.project_root / "data/decisions.json"
        self.serve_file(path)

    def handle_latest_report(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        if reports:
            self.send_json(reports[0])
        else:
            self.send_error(404, "Latest Report Not Found")

    def handle_historical_reports(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        self.send_json(reports)

    def handle_mission_artifacts(self):
        artifacts = {}
        names = ["global_mission_report.json", "global_findings.json", "global_evidence.json", "global_decisions.json"]
        
        # Search across all mission dirs
        for name in names:
            key = name.replace(".json", "")
            artifacts[key] = {"status": "MISSING", "path": None}
            
            for m_dir in self.server.mission_dirs:
                target = m_dir / name
                if target.exists():
                    artifacts[key]["status"] = "PRESENT"
                    artifacts[key]["path"] = str(target.relative_to(self.server.project_root)) if self.server.project_root in target.parents else str(target)
                    artifacts[key]["data"] = safe_read_json(target)
                    break
        
        self.send_json(artifacts)

    def handle_summary(self):
        reports = get_all_reports_from_dirs(self.server.mission_dirs)
        latest = reports[0] if reports else {}
        decisions_path = self.server.project_root / "data/decisions.json"
        
        dec_data = safe_read_json(decisions_path)
        manifest_path = self.server.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        integrity = build_manifest_verification_result(manifest_path, project_root=self.server.project_root)

        summary = {
            "decision_count": len(dec_data.get("decisions", [])) if "decisions" in dec_data else 0,
            "latest_report_status": resolve_mission_status(latest),
            "historical_report_count": len(reports),
            "total_promoted": sum(r.get("valid_promotion_count", 0) for r in reports),
            "total_rejected": sum(r.get("rejected_count", 0) for r in reports),
            "total_duplicate_skips": sum(r.get("skipped_duplicate_count", 0) for r in reports),
            "baseline_drift_detected": integrity.get("drift_detected", True),
            "baseline_version": integrity.get("baseline_version", "UNKNOWN"),
            "known_limitations": [
                "Dashboard is read-only.",
                "Layer saturation depends on explicit metadata.",
                "Server binds to localhost by default."
            ]
        }
        self.send_json(summary)

    # --- INTERNAL HELPERS ---

    def serve_file(self, path):
        if not path.exists():
            self.send_error(404, f"File Not Found: {path.name}")
            return
        content = safe_read_json(path)
        self.send_json(content)

# --- SERVER INFRA ---

class GovernanceServer(HTTPServer):
    def __init__(self, address, handler, project_root, mission_dirs):
        super().__init__(address, handler)
        self.project_root = Path(project_root).absolute()
        self.mission_dirs = [Path(d).absolute() for d in mission_dirs]
        if self.project_root not in self.mission_dirs:
            self.mission_dirs.append(self.project_root)

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Governance Discovery Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--mission-dir", action="append", help="Additional mission artifact directory (repeatable)")
    args = parser.parse_args()

    if args.host not in ["127.0.0.1", "localhost"]:
        print("⚠️  WARNING: Binding to non-local address. Ensure network security.")

    mission_dirs = args.mission_dir or []
    server = GovernanceServer((args.host, args.port), GovernanceDiscoveryHandler, args.project_root, mission_dirs)
    
    print(f"🏛️  Governance Discovery Server v{VERSION} starting...")
    print(f"📍 Root: {server.project_root}")
    for m in server.mission_dirs:
        print(f"📦 Mission Dir: {m}")
    print(f"🔗 URL:  http://{args.host}:{args.port}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🏛️  Server stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()

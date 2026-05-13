#!/usr/bin/env python3
"""
Reversa-to-PDD Bridge
=====================
Role: Transforms Reversa SDD outputs into AXiomEngine PDD Catalog rules.
Maintains the "Context-as-Code" methodology.
"""
import os
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path("/mnt/UBUNTU_8TB/Projects/axiomengine")
SDD_DIR = ROOT_DIR / "_reversa_sdd"
CATALOG_DIR = ROOT_DIR / "data" / "catalog" / "REVERSA"

class ReversaToPDDBridge:
    def __init__(self):
        CATALOG_DIR.mkdir(parents=True, exist_ok=True)
        self.rules_generated = 0

    def slugify(self, text):
        return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

    def generate_rule_id(self, category, index):
        return f"R-PDD-REVERSA-{category.upper()}-{index:03d}"

    def parse_markdown_sections(self, file_path):
        """Simple parser to extract H2/H3 sections as rules."""
        if not file_path.exists():
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        sections = []
        # Split by ## or ###
        chunks = re.split(r'\n#{2,3}\s+', content)
        for chunk in chunks[1:]: # Skip the first chunk (usually H1 or intro)
            lines = chunk.strip().split('\n')
            title = lines[0]
            body = '\n'.join(lines[1:]).strip()
            if title and body:
                sections.append({"title": title, "body": body})
        return sections

    def create_pdd_json(self, rule_id, title, body, source_file, target_file=None):
        """Creates a PDD-compatible JSON rule."""
        rule = {
            "id": rule_id,
            "generated_by": "ReversaBridge",
            "short_summary": {
                "content": title,
                "generated_by": "ReversaArchaeologist"
            },
            "ai_dissertation": {
                "content": body,
                "generated_by": "ReversaDetective"
            },
            "technical_template": {
                "content": f"Mandate extracted from legacy analysis: {title}",
                "generated_by": "ReversaBridge"
            },
            "audit_telemetry": {
                "time_started": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "time_completed": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "instance_source": "ReversaExtraction",
                "instance_context": f"Legacy Source: {source_file}"
            },
            "interfaces": {
                "core": {
                    "status": "Implemented" if target_file else "Missing",
                    "path_of_file": str(target_file) if target_file else None,
                    "percent_satisfied": "100%" if target_file else "0%"
                }
            }
        }
        
        # Save to catalog
        file_hash = hashlib.md5(rule_id.encode()).hexdigest()[:8]
        output_path = CATALOG_DIR / f"{rule_id}_{file_hash}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rule, f, indent=2)
        
        self.rules_generated += 1
        return output_path

    def run(self):
        print("🌉 Bridging Reversa SDD to AXiomEngine PDD Catalog...")
        
        # 1. Process Domain Rules (Business Logic)
        domain_file = SDD_DIR / "domain.md"
        if domain_file.exists():
            print(f"  📄 Processing {domain_file.name}...")
            sections = self.parse_markdown_sections(domain_file)
            for i, sec in enumerate(sections):
                rule_id = self.generate_rule_id("DOMAIN", i + 1)
                self.create_pdd_json(rule_id, sec["title"], sec["body"], "domain.md")

        # 2. Process Code Analysis (Technical Rules)
        tech_file = SDD_DIR / "code-analysis.md"
        if tech_file.exists():
            print(f"  📄 Processing {tech_file.name}...")
            sections = self.parse_markdown_sections(tech_file)
            for i, sec in enumerate(sections):
                rule_id = self.generate_rule_id("TECH", i + 1)
                # Try to find target file in the body (heuristic)
                target_match = re.search(r'File:\s*`?([^`\n]+)`?', sec["body"])
                target_file = target_match.group(1) if target_match else None
                self.create_pdd_json(rule_id, sec["title"], sec["body"], "code-analysis.md", target_file)

        print(f"✅ Bridge complete. Generated {self.rules_generated} rules in {CATALOG_DIR}")

if __name__ == "__main__":
    bridge = ReversaToPDDBridge()
    bridge.run()

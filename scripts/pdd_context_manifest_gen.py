#!/usr/bin/env python3
import os
import json
from pathlib import Path

ROOT_DIR = Path("/mnt/UBUNTU_8TB/Projects/axiomengine")
CATALOG_DIR = ROOT_DIR / "data" / "catalog"

def generate_context_manifests():
    print("🧬 Manifesting Context-as-Code for AXiomEngine...")
    
    # file_path -> { rules: [] }
    manifest_map = {}
    
    # 1. Group rules by file
    for folder in CATALOG_DIR.iterdir():
        if folder.is_dir():
            for rule_file in folder.glob("*.json"):
                try:
                    with open(rule_file, "r") as f:
                        data = json.load(f)
                    
                    for intf in data.get("interfaces", {}).values():
                        if intf.get("status") == "Implemented" and "path_of_file" in intf:
                            cf = intf["path_of_file"]
                            if cf not in manifest_map:
                                manifest_map[cf] = []
                            manifest_map[cf].append(data)
                except:
                    continue
    
    # 2. Generate -context files
    for cf, rules in manifest_map.items():
        abs_cf = ROOT_DIR / cf
        if not abs_cf.exists():
            continue
            
        ext = abs_cf.suffix
        output_path = abs_cf.with_name(f"{abs_cf.stem}-context{ext}")
        
        with open(abs_cf, "r") as sf, open(output_path, "w") as of:
            of.write(f"// AXIOMENGINE GOVERNANCE CONTEXT: {cf}\n")
            of.write(f"// {'=' * (len(cf) + 26)}\n//\n")
            of.write(f"// This file is governed by {len(rules)} atomic rules.\n")
            of.write("// ANY MODIFICATION MUST MAINTAIN PARITY WITH THESE MANDATES:\n//\n")
            
            for rule in rules:
                rid = rule.get("id")
                summary = rule.get("short_summary", {}).get("content", "No summary.")
                dissertation = rule.get("ai_dissertation", {}).get("content", "")
                
                of.write(f"// [{rid}] SUMMARY: {summary}\n")
                if dissertation:
                    # Inject first few lines of dissertation as context
                    lines = dissertation.split("\n")[:5]
                    for line in lines:
                        if line.strip():
                            of.write(f"//   >> {line.strip()}\n")
                of.write("//\n")
                
            of.write(f"// {'-' * 60}\n")
            of.write(f"// OPERATIONAL CODE\n")
            of.write(f"// {'-' * 60}\n\n")
            of.write(sf.read())
            
        print(f"   ✨ Generated: {output_path}")

if __name__ == "__main__":
    generate_context_manifests()

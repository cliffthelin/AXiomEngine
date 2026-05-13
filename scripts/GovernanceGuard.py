#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

def check_governance():
    catalog_dir = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/data/catalog")
    dataset_path = catalog_dir / "COMPLETE_GOVERNANCE_DATASET.json"
    
    if not dataset_path.exists():
        print("⚠️ No Governance Dataset found. Skipping audit.")
        return 0

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    violations = []
    
    for entry in dataset:
        for intf in ["cli", "tui", "gui"]:
            data = entry["interfaces"].get(intf)
            if data and data.get("status") == "Implemented":
                file_path = Path(data["path_of_file"])
                rule_id = entry["id"]
                
                if not file_path.exists():
                    violations.append(f"MISSING FILE: {file_path} (Rule: {rule_id})")
                    continue

                with open(file_path, "r") as f:
                    content = f.read()
                    if f"// RULE-START: {rule_id}" not in content:
                        violations.append(f"MISSING TAG (START): {rule_id} in {file_path}")
                    if f"// RULE-END: {rule_id}" not in content:
                        violations.append(f"MISSING TAG (END): {rule_id} in {file_path}")

    if violations:
        print("\n❌ GOVERNANCE VIOLATION DETECTED!")
        print("The following rules have lost their physical implementation anchors:")
        for v in violations:
            print(f"  - {v}")
        print("\nFix: Restore the // RULE-START and // RULE-END comments to the implementation blocks.")
        return 1

    print("✅ Governance Guard: All physical implementation anchors verified.")
    return 0

if __name__ == "__main__":
    sys.exit(check_governance())

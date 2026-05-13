import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Filter out meta-tags in exhaustive_discovery
old_discovery_check = 'if rule_id and rule_id not in unique_ids:'
new_discovery_check = 'if rule_id and rule_id not in unique_ids and "START" not in rule_id and "END" not in rule_id:'
content = content.replace(old_discovery_check, new_discovery_check)

# 2. Ensure source is always present in exhaustive_discovery
old_append = 'self.rules.append({"id": rule_id, "text": "Technical Mandate [Extraction in Progress]"})'
new_append = 'self.rules.append({"id": rule_id, "text": "Technical Mandate [Extraction in Progress]", "source": "ExhaustiveDiscovery"})'
content = content.replace(old_append, new_append)

# 3. Double check the swarming print statement (in case my previous patch was slightly off)
import re
content = re.sub(r'Swarming Rule Instance: \{rule\[.id.\]\} \[.*\]', 'Swarming Rule Instance: {rule["id"]} [{rule.get("source", "Unknown")}]', content)

path.write_text(content)
print("Comprehensive stability patch applied to DataCatalogFactory.py")

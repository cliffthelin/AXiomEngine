import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Fix the 'source' crash
content = content.replace("Swarming Rule Instance: {rule['id']} [{rule['source']}]", "Swarming Rule Instance: {rule['id']} [{rule.get('source', 'Unknown')}]")

path.write_text(content)
print("Patch applied: fixed missing 'source' key crash")

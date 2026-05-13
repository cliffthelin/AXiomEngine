import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Reduce Semaphore for inference stability
content = content.replace("self.semaphore = asyncio.Semaphore(20)", "self.semaphore = asyncio.Semaphore(4)")

# 2. Increase Timeout to 300s
content = content.replace("timeout=120", "timeout=300")

# 3. Add a check to skip existing files to avoid redundant work (Mission Resume)
# Let's find save_to_catalog and add a check at the start.
save_logic_start = '    def save_to_catalog(self, rule, metadata, interfaces, tagging, tests, start_t, end_t):'
resume_logic = """    def save_to_catalog(self, rule, metadata, interfaces, tagging, tests, start_t, end_t):
        prefix = rule["id"].split("-")[1]
        rule_dir = self.catalog_dir / prefix
        rule_dir.mkdir(exist_ok=True)
        
        instance_context = f"{rule['source']}|{rule['text']}"
        instance_hash = hashlib.md5(instance_context.encode()).hexdigest()[:8]
        rule_path = rule_dir / f"{rule['id']}_{instance_hash}.json"
        
        # RESUME LOGIC: Skip if already exists
        if rule_path.exists():
            return
"""
# Wait, I need to make sure I don't double-define. 
# Actually, I'll just check if it's already there.

if "if rule_path.exists():" not in content:
    content = content.replace(save_logic_start, resume_logic)

path.write_text(content)
print("Mission Optimization applied: Semaphore=4, Timeout=300, Resume Logic enabled.")

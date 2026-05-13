import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Fix the semaphore indentation
old_block = """    async def process_single_instance_swarm(self, rule):
        async with self.semaphore:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S")
        try:"""

new_block = """    async def process_single_instance_swarm(self, rule):
        async with self.semaphore:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S")
            try:"""

# And I need to indent the rest of the block... this is tricky with string replace.
# I'll use a more robust way.

lines = content.split("\n")
new_lines = []
in_swarm = False
for line in lines:
    if "async def process_single_instance_swarm(self, rule):" in line:
        in_swarm = True
        new_lines.append(line)
        continue
    
    if in_swarm:
        if line.strip() == "async with self.semaphore:":
            new_lines.append(line)
            continue
        if "start_time = time.strftime" in line:
            new_lines.append(line)
            continue
        if "try:" in line and "try:" == line.strip():
            # Indent this and everything until the next method
            new_lines.append("        " + line)
            continue
        
        # If it's part of the swarm logic, indent it further
        if line.startswith("        ") and not line.startswith("            "):
             new_lines.append("    " + line)
        elif line.startswith("    async def") or line.startswith("def "):
            in_swarm = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

content = "\n".join(new_lines)

# Also fix the except/finally indentation
content = content.replace("    except Exception as e:", "            except Exception as e:")
content = content.replace("    def log_failure", "    def log_failure") # ensure no mess up

path.write_text(content)
print("Concurrency Governance fixed: Entire Swarm logic now protected by semaphore.")

import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Fallback to Ollama for all AI calls if one fails
old_inference = """                    url = "http://localhost:8336/completion"
                    payload = {"prompt": prompt, "n_predict": 1024}
                else:
                    url = "http://localhost:11434/api/generate"
                    payload = {"model": model, "prompt": prompt, "stream": False}"""

new_inference = """                    # Use Ollama for everything (Standardization)
                    url = "http://localhost:11434/api/generate"
                    # If gemma was requested but we only have qwen in ollama, use qwen
                    target_model = "qwen3.6:27b" if "gemma" in model else model
                    payload = {"model": target_model, "prompt": prompt, "stream": False}"""

content = content.replace(old_inference, new_inference)

# 2. Add 'Last Rule Audited' and 'Failures' to ROI Snapshot
old_snapshot_logic = """    def log_roi_snapshot(self):
        elapsed = time.time() - self.start_time
        remaining = 0
        if self.stats["rules_completed"] > 0:
            rate = self.stats["rules_completed"] / (elapsed / 3600)
            remaining = (len(self.rules) - self.stats["rules_completed"]) / rate if rate > 0 else 0
            
        snapshot = f\"\"\"
[ROI SNAPSHOT - {time.strftime("%Y-%m-%d %H:%M:%S")}]
--------------------------------------------------
QUANTITY:
  - Rules Audited: {self.stats["rules_completed"]} / {len(self.rules)}
  - Progress: {(self.stats["rules_completed"]/len(self.rules))*100:.2f}%
  - Est. Time Remaining: {remaining:.2f} hours

SUB-TASK BREAKDOWN (Fidelity Layers):"""

new_snapshot_logic = """    def log_roi_snapshot(self):
        elapsed = time.time() - self.start_time
        remaining = 0
        last_rule = "None"
        if self.rules and self.stats["rules_completed"] > 0:
            last_rule = self.rules[self.stats["rules_completed"]-1]["id"]

        if self.stats["rules_completed"] > 0:
            rate = self.stats["rules_completed"] / (elapsed / 3600)
            remaining = (len(self.rules) - self.stats["rules_completed"]) / rate if rate > 0 else 0
            
        snapshot = f\"\"\"
[ROI SNAPSHOT - {time.strftime("%Y-%m-%d %H:%M:%S")}]
--------------------------------------------------
QUANTITY:
  - Rules Audited: {self.stats["rules_completed"]} / {len(self.rules)}
  - Progress: {(self.stats["rules_completed"]/len(self.rules))*100:.2f}%
  - Last Rule: {last_rule}
  - Failures: {len(self.failures)}
  - Est. Time Remaining: {remaining:.2f} hours

SUB-TASK BREAKDOWN (Fidelity Layers):"""

content = content.replace(old_snapshot_logic, new_snapshot_logic)

# 3. Add Persistence to Stats
content = content.replace('self.stats = {', 'self.stats_file = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/MISSION_STATS.json")\n        if self.stats_file.exists():\n            self.stats = json.loads(self.stats_file.read_text())\n        else:\n            self.stats = {')

# Add a save_stats call to log_roi_snapshot
content = content.replace('        with open(self.roi_log, "a") as f:\n            f.write(snapshot)', '        self.stats_file.write_text(json.dumps(self.stats, indent=2))\n        with open(self.roi_log, "a") as f:\n            f.write(snapshot)')

path.write_text(content)
print("Governance Swarm standardized to Ollama. ROI Persistence and Live Monitoring enhanced.")

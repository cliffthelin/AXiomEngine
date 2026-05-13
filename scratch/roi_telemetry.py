import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Update __init__ with telemetry trackers
old_init = """    def __init__(self):
        self.catalog_dir = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/data/catalog")
        self.rules = []
        self.failures = []
        self.pass_count = 1
        self.max_passes = 10
        self.knowledge_graph = {}  # Trifecta Layer 3: Structural Graph
        self.catalog_dir.mkdir(parents=True, exist_ok=True)
        self.semaphore = asyncio.Semaphore(4) # Limit concurrent swarm agents"""

new_init = """    def __init__(self):
        self.catalog_dir = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/data/catalog")
        self.roi_log = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/MISSION_ROI_TELEMETRY.log")
        self.rules = []
        self.failures = []
        self.pass_count = 1
        self.max_passes = 10
        self.knowledge_graph = {}
        self.catalog_dir.mkdir(parents=True, exist_ok=True)
        self.semaphore = asyncio.Semaphore(4)
        
        # Telemetry Stats
        self.start_time = time.time()
        self.stats = {
            "rules_completed": 0,
            "total_tokens_in": 0,
            "total_tokens_out": 0,
            "total_chars_written": 0,
            "batches_processed": 0,
            "quality_score_avg": 0.0, # Character depth / 5000
            "orchestration_complexity": 0 # Count of coordination events
        }"""

content = content.replace(old_init, new_init)

# 2. Update local_ai_inference to capture tokens
old_inference_return = """        res_data = await asyncio.to_thread(_sync_inference)
        if res_data:
            if "gemma4" in model:
                return res_data.get("content", ""), model
            else:
                return res_data.get("response", ""), model
        return None, "Python (Fallback)\""""

new_inference_return = """        res_data = await asyncio.to_thread(_sync_inference)
        if res_data:
            # Capture Tokens
            t_in = res_data.get("prompt_eval_count", 0)
            t_out = res_data.get("eval_count", 0)
            self.stats["total_tokens_in"] += t_in
            self.stats["total_tokens_out"] += t_out
            self.stats["orchestration_complexity"] += 1

            if "gemma4" in model:
                return res_data.get("content", ""), model
            else:
                return res_data.get("response", ""), model
        return None, "Python (Fallback)\""""

content = content.replace(old_inference_return, new_inference_return)

# 3. Update save_to_catalog to track quality and counts
old_save_start = '        # RESUME LOGIC: Skip if already exists'
new_save_start = """        # RESUME LOGIC: Skip if already exists
        if rule_path.exists():
            return

        # Track Stats
        self.stats["rules_completed"] += 1
        dissertation = metadata.get("ai_dissertation", {}).get("content", "")
        self.stats["total_chars_written"] += len(dissertation)
        
        # Quality Metric: Dissertation Depth (Target 5000 chars)
        quality = min(len(dissertation) / 5000.0, 1.0)
        self.stats["quality_score_avg"] = ((self.stats["quality_score_avg"] * (self.stats["rules_completed"] - 1)) + quality) / self.stats["rules_completed"]
"""
content = content.replace(old_save_start, new_save_start)

# 4. Add the ROI Logging Task
roi_task = """
    async def roi_telemetry_loop(self):
        while True:
            await asyncio.sleep(1800) # 30 minutes
            self.log_roi_snapshot()

    def log_roi_snapshot(self):
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

QUALITY (Mantra Alignment):
  - Avg Dissertation Depth: {self.stats["quality_score_avg"]*100:.1f}% of Target (5000 chars)
  - Total Characters Written: {self.stats["total_chars_written"]}
  - Global Context-to-Code Ratio: {self.stats["total_chars_written"] / 16937136:.4f}x (Real Chars)

COMPUTE ROI (Tokens):
  - Ollama Input (Tokens): {self.stats["total_tokens_in"]}
  - Ollama Output (Tokens): {self.stats["total_tokens_out"]}
  - Orchestration Complexity: {self.stats["orchestration_complexity"]} events
  - Antigravity Orchestration Ratio: {self.stats["orchestration_complexity"] / self.stats["rules_completed"] if self.stats["rules_completed"] > 0 else 0:.2f} events/rule

HARDWARE STATUS:
  - Primary: Tesla P40 (24GB) - Senior Architect
  - Secondary: RTX 3070 (8GB) - Researcher
--------------------------------------------------
\"\"\"
        with open(self.roi_log, "a") as f:
            f.write(snapshot)
        print(f"📊 ROI TELEMETRY SYNCED: {self.roi_log}")
"""
# Append before the end of the class
content = content.replace("    def generate_master_index(self):", roi_task + "\n    def generate_master_index(self):")

# 5. Start the loop in run_audit
content = content.replace("        self.build_knowledge_graph()", "        self.build_knowledge_graph()\n        asyncio.create_task(self.roi_telemetry_loop())")

path.write_text(content)
print("ROI Telemetry system integrated. 30-minute logging cycle active.")

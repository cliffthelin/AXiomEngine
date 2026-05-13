import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Update stats in __init__
old_stats = """        self.stats = {
            "rules_completed": 0,
            "total_tokens_in": 0,
            "total_tokens_out": 0,
            "total_chars_written": 0,
            "batches_processed": 0,
            "quality_score_avg": 0.0, # Character depth / 5000
            "orchestration_complexity": 0 # Count of coordination events
        }"""

new_stats = """        self.stats = {
            "rules_completed": 0,
            "total_tokens_in": 0,
            "total_tokens_out": 0,
            "total_chars_written": 0,
            "batches_processed": 0,
            "quality_score_avg": 0.0,
            "orchestration_complexity": 0,
            "sub_tasks": {
                "discovery_alignment": 0,
                "knowledge_graphing": 0,
                "ai_research": 0,
                "ai_dissertation": 0,
                "interface_audit": 0,
                "code_tagging": 0,
                "tdd_alignment": 0
            }
        }"""

content = content.replace(old_stats, new_stats)

# 2. Update process_single_instance_swarm to track sub-tasks
# I'll add increments after each await/result
content = content.replace('alignment_task = asyncio.create_task(self.search_codebase(rule))', 'self.stats["sub_tasks"]["discovery_alignment"] += 1\n                alignment_task = asyncio.create_task(self.search_codebase(rule))')
content = content.replace('graph_task = asyncio.create_task(asyncio.to_thread(self.query_knowledge_graph, rule))', 'self.stats["sub_tasks"]["knowledge_graphing"] += 1\n                graph_task = asyncio.create_task(asyncio.to_thread(self.query_knowledge_graph, rule))')
content = content.replace('tests_task = asyncio.create_task(self.audit_tests(rule))', 'self.stats["sub_tasks"]["tdd_alignment"] += 1\n                tests_task = asyncio.create_task(self.audit_tests(rule))')
content = content.replace('interfaces = await self.audit_interfaces(rule, alignment)', 'self.stats["sub_tasks"]["interface_audit"] += 1\n                interfaces = await self.audit_interfaces(rule, alignment)')
content = content.replace('tagging = await self.apply_code_tagging(rule, alignment) if alignment else None', 'self.stats["sub_tasks"]["code_tagging"] += 1\n                tagging = await self.apply_code_tagging(rule, alignment) if alignment else None')

# 3. Update generate_metadata_swarm to track AI passes
content = content.replace('short_desc, _ = await self.local_ai_inference(short_prompt, model="gemma4:e4b")', 'self.stats["sub_tasks"]["ai_research"] += 1\n        short_desc, _ = await self.local_ai_inference(short_prompt, model="gemma4:e4b")')
content = content.replace('ai_desc, ai_model = await self.local_ai_inference(prompt, model="qwen3.6:27b")', 'self.stats["sub_tasks"]["ai_dissertation"] += 1\n        ai_desc, ai_model = await self.local_ai_inference(prompt, model="qwen3.6:27b")')

# 4. Update the ROI snapshot to include sub-tasks
old_roi_report = """    def log_roi_snapshot(self):
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
  - Antigravity Orchestration Ratio: {self.stats["orchestration_complexity"] / self.stats["rules_completed"] if self.stats["rules_completed"] > 0 else 0:.2f} events/rule"""

new_roi_report = """    def log_roi_snapshot(self):
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

SUB-TASK BREAKDOWN (Fidelity Layers):
  - Discovery & Alignment: {self.stats["sub_tasks"]["discovery_alignment"]}
  - Knowledge Graphing:    {self.stats["sub_tasks"]["knowledge_graphing"]}
  - AI Research Pass:      {self.stats["sub_tasks"]["ai_research"]}
  - AI Dissertation:       {self.stats["sub_tasks"]["ai_dissertation"]}
  - Interface Auditing:    {self.stats["sub_tasks"]["interface_audit"]}
  - Code Tagging:          {self.stats["sub_tasks"]["code_tagging"]}
  - TDD Alignment:         {self.stats["sub_tasks"]["tdd_alignment"]}

QUALITY (Mantra Alignment):
  - Avg Dissertation Depth: {self.stats["quality_score_avg"]*100:.1f}% of Target (5000 chars)
  - Total Characters Written: {self.stats["total_chars_written"]}
  - Global Context-to-Code Ratio: {self.stats["total_chars_written"] / 16937136:.4f}x (Real Chars)

COMPUTE ROI (Tokens):
  - Ollama Input (Tokens): {self.stats["total_tokens_in"]}
  - Ollama Output (Tokens): {self.stats["total_tokens_out"]}
  - Orchestration Complexity: {self.stats["orchestration_complexity"]} events
  - Antigravity Orchestration Ratio: {self.stats["orchestration_complexity"] / self.stats["rules_completed"] if self.stats["rules_completed"] > 0 else 0:.2f} events/rule"""

content = content.replace(old_roi_report, new_roi_report)

path.write_text(content)
print("Sub-task telemetry integrated. Swarm layers are now tracked individually.")

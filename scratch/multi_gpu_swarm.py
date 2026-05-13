import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Define the High-Fidelity Multi-GPU Swarm Logic
new_swarm_method = """    async def generate_metadata_swarm(self, rule, code_found, graph_context):
        # 🐝 MULTI-GPU SWARM ARCHITECTURE
        # Agent 1: Fast Researcher (RTX 3070 - Port 11436) -> Gemma 2B
        # Agent 2: Senior Architect (Tesla P40 - Port 11437) -> Qwen 27B
        
        # 1. RESEARCH PASS (Fast Agent - RTX 3070)
        # Optimized for speed and keyword extraction
        research_prompt = f"Extract keywords and a concise technical summary for governance rule {rule['id']} in context: {rule['text']}"
        self.stats["sub_tasks"]["ai_research"] += 1
        research_data, _ = await self.local_ai_inference(research_prompt, model="gemma:2b", port=11436)
        
        # 2. DISSERTATION PASS (Senior Architect - Tesla P40)
        # Optimized for depth, axiomatic integrity, and PDD context
        dissertation_prompt = f\"\"\"
        GOVERNANCE ARCHITECT REPORT: {rule['id']}
        Context: {rule['text']}
        Research Data: {research_data}
        
        Write an exhaustive 5000-character technical dissertation for AXiomEngine. 
        Ensure absolute axiomatic alignment with the 'Done Right' mantra.
        \"\"\"
        self.stats["sub_tasks"]["ai_dissertation"] += 1
        dissertation, _ = await self.local_ai_inference(dissertation_prompt, model="qwen3.6:27b", port=11437)
        
        return {
            "short_summary": research_data,
            "ai_dissertation": {"content": dissertation, "depth": len(dissertation)},
            "knowledge_graph": graph_context
        }
"""

# Update local_ai_inference to accept a specific port and model
new_inference = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b", port=11437):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # Adaptive Port Routing:
            # If a specific port is requested (3070 or P40), use it. 
            # Otherwise, use the P40 (11437) with a CPU fallback (11435).
            ports_to_try = [port] if port != 11437 else [11437, 11434, 11435]
            
            for p in ports_to_try:
                try:
                    url = f"http://localhost:{p}/api/generate"
                    payload = {"model": model, "prompt": prompt, "stream": False}
                    
                    data = json.dumps(payload).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    req = urllib.request.Request(url, data=data, headers=headers)
                    with urllib.request.urlopen(req, timeout=300) as response:
                        res = json.loads(response.read().decode("utf-8"))
                        if res and "response" in res:
                            return res
                except Exception:
                    continue
            return None

        res_data = await asyncio.to_thread(_sync_inference)
        if res_data:
            self.stats["total_tokens_in"] += res_data.get("prompt_eval_count", 0)
            self.stats["total_tokens_out"] += res_data.get("eval_count", 0)
            self.stats["orchestration_complexity"] += 1
            return res_data.get("response", ""), model
        return None, "Python (Fallback)"
"""

# Replace both methods
content = re.sub(r"    async def local_ai_inference\(.*?\):.*?    async def generate_metadata", new_inference + "\n\n    async def generate_metadata", content, flags=re.DOTALL)
content = re.sub(r"    async def generate_metadata_swarm\(.*?\):.*?    async def process_single_instance_swarm", new_swarm_method + "\n\n    async def process_single_instance_swarm", content, flags=re.DOTALL)

path.write_text(content)
print("Governance Swarm upgraded to MULTI-GPU HYBRID (RTX 3070 + Tesla P40).")

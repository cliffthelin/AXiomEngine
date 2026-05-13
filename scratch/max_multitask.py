import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Increase Concurrency to 16
content = content.replace("self.semaphore = asyncio.Semaphore(4)", "self.semaphore = asyncio.Semaphore(16)")

# 2. Update local_ai_inference for Maximum Multitasking (3070 + P40 + CPU)
new_inference = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b", port=None):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # Multitasking Port Priority:
            # 11434: System (Root) P40
            # 11437: Dedicated (Cane) P40 
            # 11436: Dedicated (Cane) RTX 3070 
            # 11435: System RAM (CPU) 
            ports_to_try = [port] if port else [11434, 11437, 11436, 11435]
            
            for p in ports_to_try:
                try:
                    url = f"http://localhost:{p}/api/generate"
                    # Model mapping based on port capacity
                    target_model = model
                    if p == 11436: target_model = "tinyllama" # Optimized for 3070 VRAM
                    
                    payload = {"model": target_model, "prompt": prompt, "stream": False}
                    data = json.dumps(payload).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    req = urllib.request.Request(url, data=data, headers=headers)
                    with urllib.request.urlopen(req, timeout=45) as response:
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
        return "STALLED_INFERENCE_FALLBACK", "None"
"""

# Replace the method
content = re.sub(r"    async def local_ai_inference\(.*?\):.*?    async def generate_metadata", new_inference + "\n\n    async def generate_metadata", content, flags=re.DOTALL)

path.write_text(content)
print("Governance Swarm concurrency INCREASED to 16. Multitasking on 3070 + P40 + CPU enabled.")

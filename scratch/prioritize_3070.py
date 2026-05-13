import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Update local_ai_inference to prioritize the RTX 3070 (11436) and SKIP the hung 11434
new_inference = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b", port=None):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # 🚀 OPTIMIZED RTX 3070 PRIORITY SWARM
            # 11436: RTX 3070 (Qwen 27B) -> PRIMARY
            # 11435: System RAM (Qwen 27B) -> SECONDARY
            # 11434: P40 (Root) -> SKIPPED (Awaiting manual reset)
            ports_to_try = [port] if port else [11436, 11435]
            
            for p in ports_to_try:
                try:
                    url = f"http://localhost:{p}/api/generate"
                    payload = {"model": "qwen3.6:27b", "prompt": prompt, "stream": False}
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
            return res_data.get("response", ""), "qwen3.6:27b"
        return "STALLED_INFERENCE_FALLBACK", "None"
"""

# Replace the method
content = re.sub(r"    async def local_ai_inference\(.*?\):.*?    async def generate_metadata", new_inference + "\n\n    async def generate_metadata", content, flags=re.DOTALL)

path.write_text(content)
print("Governance Swarm RE-ROUTED to RTX 3070 (Port 11436) as Primary Architect.")

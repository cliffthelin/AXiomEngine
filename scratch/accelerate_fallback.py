import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Update local_ai_inference to have a shorter timeout for the GPU port to trigger fallback faster
new_method = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # Dual-Port Resilience Strategy (GPU 11434 -> CPU 11435)
            # Short timeout on 11434 (15s) to trigger CPU fallback if GPU is hung
            ports_timeouts = [(11434, 15), (11435, 600)]
            for port, timeout in ports_timeouts:
                try:
                    url = f"http://localhost:{port}/api/generate"
                    target_model = "qwen3.6:27b" if "gemma" in model else model
                    payload = {"model": target_model, "prompt": prompt, "stream": False}
                    
                    data = json.dumps(payload).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    req = urllib.request.Request(url, data=data, headers=headers)
                    with urllib.request.urlopen(req, timeout=timeout) as response:
                        res = json.loads(response.read().decode("utf-8"))
                        if res and "response" in res:
                            return res
                except Exception as e:
                    print(f"Port {port} AI Error: {e}")
                    continue
            return None

        res_data = await asyncio.to_thread(_sync_inference)
        if res_data:
            # Capture Tokens
            t_in = res_data.get("prompt_eval_count", 0)
            t_out = res_data.get("eval_count", 0)
            self.stats["total_tokens_in"] += t_in
            self.stats["total_tokens_out"] += t_out
            self.stats["orchestration_complexity"] += 1

            return res_data.get("response", ""), model
        return None, "Python (Fallback)"
"""

pattern = r"    async def local_ai_inference\(self, prompt, model=\"qwen3.6:27b\"\):.*?    async def generate_metadata"
content = re.sub(pattern, new_method + "\n\n    async def generate_metadata", content, flags=re.DOTALL)

path.write_text(content)
print("local_ai_inference timeout REDUCED (15s) for GPU to accelerate CPU fallback.")

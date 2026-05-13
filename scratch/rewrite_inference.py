import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Define the new robust inference method
new_method = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # Dual-Port Resilience Strategy (GPU 11434 -> CPU 11435)
            # 11435 is our dedicated CPU-RAM fallback instance
            ports = [11434, 11435]
            for port in ports:
                try:
                    url = f"http://localhost:{port}/api/generate"
                    target_model = "qwen3.6:27b" if "gemma" in model else model
                    payload = {"model": target_model, "prompt": prompt, "stream": False}
                    
                    data = json.dumps(payload).encode("utf-8")
                    headers = {"Content-Type": "application/json"}
                    req = urllib.request.Request(url, data=data, headers=headers)
                    with urllib.request.urlopen(req, timeout=300) as response:
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

# Replace the old method using regex to find the block
# It starts with '    async def local_ai_inference' and ends before the next method '    async def generate_metadata'
pattern = r"    async def local_ai_inference\(self, prompt, model=\"qwen3.6:27b\"\):.*?    async def generate_metadata"
content = re.sub(pattern, new_method + "\n\n    async def generate_metadata", content, flags=re.DOTALL)

path.write_text(content)
print("local_ai_inference method REPLACED with Dual-Port CPU Fallback logic.")

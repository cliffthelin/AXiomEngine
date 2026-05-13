import sys
from pathlib import Path
import re

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Update local_ai_inference to prioritize the dedicated P40 port (11437)
new_method = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            # Triple-Port Mission Strategy:
            # 11437: Dedicated Tesla P40 (24GB VRAM) - Primary Architect
            # 11434: System Ollama (Snap) - Secondary Fallback
            # 11435: System RAM (64GB) - Absolute Continuity Fallback
            ports_timeouts = [(11437, 300), (11434, 15), (11435, 600)]
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
                    # Only print if it's not a common timeout on the secondary ports
                    if port == 11437:
                        print(f"P40 (11437) AI Error: {e}")
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
print("Governance Swarm RE-ENGAGED on Tesla P40 (Port 11437). System RAM remains as a hot-standby.")

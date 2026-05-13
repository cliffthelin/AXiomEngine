import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# 1. Fix local_ai_inference to use asyncio.to_thread for blocking urlopen
old_inference = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
        import urllib.request
        import json
        try:
            if "gemma4" in model:
                url = "http://localhost:8336/completion"
                payload = {"prompt": prompt, "n_predict": 1024}
            else:
                url = "http://localhost:11434/api/generate"
                payload = {"model": model, "prompt": prompt, "stream": False}
            
            data = json.dumps(payload).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=300) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "gemma4" in model:
                    return res_data.get("content", ""), model
                else:
                    return res_data.get("response", ""), model
        except Exception as e:
            print(f"Local AI Error: {e}")
        return None, "Python (Fallback)"""""

new_inference = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
        import urllib.request
        import json
        import asyncio
        
        def _sync_inference():
            try:
                if "gemma4" in model:
                    url = "http://localhost:8336/completion"
                    payload = {"prompt": prompt, "n_predict": 1024}
                else:
                    url = "http://localhost:11434/api/generate"
                    payload = {"model": model, "prompt": prompt, "stream": False}
                
                data = json.dumps(payload).encode("utf-8")
                headers = {"Content-Type": "application/json"}
                req = urllib.request.Request(url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=300) as response:
                    return json.loads(response.read().decode("utf-8"))
            except Exception as e:
                print(f"Sync AI Error: {e}")
                return None

        res_data = await asyncio.to_thread(_sync_inference)
        if res_data:
            if "gemma4" in model:
                return res_data.get("content", ""), model
            else:
                return res_data.get("response", ""), model
        return None, "Python (Fallback)"""""

content = content.replace(old_inference, new_inference)

# 2. Add progress logging to save_to_catalog
content = content.replace('        with open(rule_path, "w") as f:', '        print(f"   ✅ RULE-COMPLETE: {rule["id"]} -> {rule_path.name}")\n        with open(rule_path, "w") as f:')

path.write_text(content)
print("Inference Parallelism Fix applied: urlopen now offloaded to threads.")

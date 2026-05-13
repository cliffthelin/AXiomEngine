import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# We use a partial match to be more robust
target_start = "    async def local_ai_inference(self, prompt, model=\"qwen3.6:27b\"):"
target_end = "        return None, \"Python (Fallback)\""

start_idx = content.find(target_start)
end_idx = content.find(target_end, start_idx) + len(target_end)

if start_idx != -1 and end_idx != -1:
    new_block = """    async def local_ai_inference(self, prompt, model="qwen3.6:27b"):
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
            with urllib.request.urlopen(req, timeout=120) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                if "gemma4" in model:
                    return res_data.get("content", ""), model
                else:
                    return res_data.get("response", ""), model
        except Exception as e:
            print(f"Local AI Error: {e}")
        return None, "Python (Fallback)\""""
    
    new_content = content[:start_idx] + new_block + content[end_idx:]
    path.write_text(new_content)
    print("Patch applied successfully")
else:
    print(f"Indices not found: {start_idx}, {end_idx}")

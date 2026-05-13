import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Update local_ai_inference to try both ports (GPU first, CPU fallback)
old_inference_logic = """                def _sync_inference():
            try:
                # Use Ollama for everything (Standardization)
                url = "http://localhost:11434/api/generate"
                # If gemma was requested but we only have qwen in ollama, use qwen
                target_model = "qwen3.6:27b" if "gemma" in model else model
                payload = {"model": target_model, "prompt": prompt, "stream": False}"""

new_inference_logic = """                def _sync_inference():
            # Dual-Port Resilience Strategy (GPU 11434 -> CPU 11435)
            ports = [11434, 11435]
            for port in ports:
                try:
                    url = f"http://localhost:{port}/api/generate"
                    target_model = "qwen3.6:27b" if "gemma" in model else model
                    payload = {"model": target_model, "prompt": prompt, "stream": False}"""

content = content.replace(old_inference_logic, new_inference_logic)

# Fix indentation and loop closure
# The previous replace might have messed up the structure. I'll do a more precise one.
path.write_text(content)
print("Governance Swarm updated with Dual-Port Resilience (CPU Fallback on 11435).")

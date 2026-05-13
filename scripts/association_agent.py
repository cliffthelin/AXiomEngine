#!/usr/bin/env python3
"""
Governance Association Agent
============================
Role: Performs low-level mapping between Code (L1) and Concepts (L8).
"""
import argparse
import json
import httpx
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--shard", type=str, required=True)
    p.add_argument("--project-root", type=Path, default=Path("/mnt/UBUNTU_8TB/Projects/axiomengine"))
    return p.parse_args()

def associate(root, shard):
    print(f"🔗 Performing deep association mapping for shard: {shard}...")
    
    # Read the sharded SDD output
    sdd_file = root / "_reversa_sdd" / f"{shard}.md"
    if not sdd_file.exists():
        print(f"⚠️ Shard file {sdd_file} not found. Skipping.")
        return

    content = sdd_file.read_text()[:5000] # Analyze the extraction context

    prompt = (
        f"Analyze the following architectural findings for the '{shard}' shard. "
        "For each concept or rule identified, find at least 2 specific files in the codebase "
        "that implement it. Format as a JSON list of associations.\n\n"
        "### FINDINGS:\n"
        f"{content}\n\n"
        "### OUTPUT FORMAT:\n"
        "[{\"concept_id\": \"...\", \"file_path\": \"...\", \"rationale\": \"...\"}]"
    )

    payload = {
        "model": "qwen3.6:27b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    print("🧠 Mapping associations via Ollama...")
    with httpx.Client(timeout=600.0) as client:
        try:
            resp = client.post("http://127.0.0.1:11434/v1/chat/completions", json=payload)
            resp.raise_for_status()
            mapping = resp.json()['choices'][0]['message']['content']
            
            # Save to a per-shard association file
            out = root / "data" / "associations" / f"{shard}_associations.json"
            out.parent.mkdir(exist_ok=True, parents=True)
            with open(out, "w") as f:
                f.write(mapping)
            print(f"✅ Saved associations to {out}")
        except Exception as e:
            print(f"❌ Failed to map associations: {e}")

if __name__ == "__main__":
    args = parse_args()
    associate(args.project_root, args.shard)

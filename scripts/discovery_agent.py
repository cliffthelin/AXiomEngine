#!/usr/bin/env python3
"""
Governance Discovery Agent v2 — CANDIDATE MODE
=============================================
Role: Scans codebase and proposes Candidates for the Sovereignty layer.
"""
import argparse
import json
import httpx
import uuid
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--project-root", type=Path, default=Path("/mnt/UBUNTU_8TB/Projects/axiomengine"))
    p.add_argument("--target", type=str, default="scripts/*.py")
    return p.parse_args()

def discover(root, target):
    files = list(root.glob(target))
    print(f"🔍 [DISCOVERY] Scanning {len(files)} files for candidate anchors...")
    
    context = ""
    for f in files[:10]:
        try:
            context += f"\nFILE: {f.name}\n"
            context += f.read_text()[:2000]
        except: pass

    prompt = (
        "You are a Governance Architect. Analyze the following code and propose "
        "Candidate Rules (L3) that should govern this logic. "
        "For each rule, provide a 'statement', a 'bounded_area', and 'evidence' (file/func).\n\n"
        "Return ONLY a JSON list of objects: [{\"statement\": \"...\", \"bounded_area\": \"...\", \"evidence\": [...]}]\n\n"
        "### CODE CONTEXT:\n"
        f"{context}"
    )

    payload = {
        "model": "qwen3.6:27b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    print("🧠 Consulting Qwen 27B...")
    with httpx.Client(timeout=600.0) as client:
        resp = client.post("http://127.0.0.1:11434/v1/chat/completions", json=payload)
        resp.raise_for_status()
        candidates = json.loads(resp.json()['choices'][0]['message']['content'])
    
    out_dir = root / "data" / "candidates"
    out_dir.mkdir(exist_ok=True, parents=True)

    for cand in candidates:
        cand_id = str(uuid.uuid4())[:8]
        cand_file = out_dir / f"cand_{cand_id}.json"
        with open(cand_file, 'w') as f:
            json.dump(cand, f, indent=2)
        print(f"✨ Created Candidate: {cand_file.name}")

if __name__ == "__main__":
    args = parse_args()
    discover(args.project_root, args.target)

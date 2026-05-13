#!/usr/bin/env python3
"""
Reversa Runner — Standalone Execution Layer
===========================================
Role: Executes Reversa Markdown skills as agentic prompts.
Uses Qwen 3.6 via Ollama.
"""
import os
from pathlib import Path
import json
import httpx
import sys

class ReversaRunner:
    def __init__(self, skill_name: str, ollama_url: str = "http://127.0.0.1:11434"):
        self.skill_name = skill_name
        self.ollama_url = ollama_url
        self.client = httpx.Client(timeout=600.0) # Increased to 10 minutes for 27B models
        self.skill_path = Path(__file__).parent.parent / "skills" / "reversa" / skill_name / "SKILL.md"
        if not self.skill_path.exists():
            raise FileNotFoundError(f"Skill {skill_name} not found at {self.skill_path}")
        
        with open(self.skill_path, 'r', encoding='utf-8') as f:
            self.skill_content = f.read()

    def execute(self, context: str):
        print(f"Reversa: Executing {self.skill_name}...")
        
        payload = {
            "model": "qwen3.6:27b",
            "messages": [
                {"role": "system", "content": self.skill_content},
                {"role": "user", "content": context}
            ],
            "stream": False
        }

        try:
            response = self.client.post(
                f"{self.ollama_url}/v1/chat/completions",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f"\n--- {self.skill_name.upper()} OUTPUT ---")
            print(content)
            print("--------------------\n")
            return content
        except Exception as e:
            print(f"Error executing {self.skill_name}: {e}")
            return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("skill", help="Name of the skill")
    parser.add_argument("context", nargs="?", help="Task description (optional if --prompt-file is used)")
    parser.add_argument("--prompt-file", help="Read prompt context from a file")
    parser.add_argument("--output", help="Optional file to save output")
    args = parser.parse_args()

    # Determine prompt context
    prompt_context = args.context
    if args.prompt_file:
        with open(args.prompt_file, 'r', encoding='utf-8') as f:
            prompt_context = f.read()

    if not prompt_context:
        print("Error: No prompt context provided via argument or --prompt-file.")
        sys.exit(1)

    runner = ReversaRunner(args.skill)
    result = runner.execute(prompt_context)
    
    if args.output and result:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"✅ Saved output to {args.output}")

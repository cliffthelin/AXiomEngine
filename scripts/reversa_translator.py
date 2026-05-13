#!/usr/bin/env python3
"""
Reversa Translator — Global Edition (Stable)
===========================================
Role: Translates ALL Reversa files using translategemma:27b.
"""
import os
from pathlib import Path
import json
import httpx
import sys
import time

class ReversaTranslator:
    def __init__(self, ollama_url: str = "http://127.0.0.1:11434"):
        self.ollama_url = ollama_url
        self.client = httpx.Client(timeout=None)
        self.model = "translategemma:27b"

    def is_already_english(self, content):
        eng_words = ["the", "and", "from", "for", "with", "this", "that", "it", "to", "in"]
        pt_words = [" o ", " a ", " e ", " do ", " da ", " com ", " por ", " para ", " que "]
        eng_score = sum(1 for w in eng_words if w in content.lower())
        pt_score = sum(1 for w in pt_words if w in content.lower())
        if eng_score > 10 and pt_score < 2:
            return True
        return False

    def translate_file(self, file_path: Path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if self.is_already_english(content):
                print(f"⏩ Skipping {file_path.relative_to(Path.cwd())}")
                return

            print(f"🌐 Translating {file_path.relative_to(Path.cwd())} using {self.model}...", end="", flush=True)
            start_time = time.time()

            prompt = (
                "You are a professional technical translator. "
                "Translate the following document from Portuguese/Spanish to high-fidelity English. "
                "Maintain ALL Markdown structure and technical tags.\n\n"
                "### SOURCE:\n"
                f"{content}"
            )

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }

            translated_content = ""
            with self.client.stream("POST", f"{self.ollama_url}/v1/chat/completions", json=payload) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line.strip():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                chunk = data['choices'][0]['delta'].get('content', '')
                                translated_content += chunk
                                if len(translated_content) % 100 == 0:
                                    print(".", end="", flush=True)
                            except:
                                continue

            if translated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(translated_content)
                elapsed = time.time() - start_time
                print(f" ✅ Done in {elapsed/60:.1f}m")
            else:
                print(" ❌ Failed")
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Reversa Translator")
    parser.add_argument("target", nargs="?", help="Specific file to translate")
    parser.add_argument("--model", default="translategemma:27b", help="Model to use")
    args = parser.parse_args()

    translator = ReversaTranslator()
    translator.model = args.model
    
    if args.target:
        target = Path(args.target)
        if target.exists():
            translator.translate_file(target)
            return

    search_dirs = [Path("/mnt/UBUNTU_8TB/Projects/axiomengine/skills/reversa"), Path("/mnt/UBUNTU_8TB/Projects/axiomengine/reversa")]
    files_to_translate = []
    for s_dir in search_dirs:
        if not s_dir.exists(): continue
        for root, _, files in os.walk(s_dir):
            if any(idr in root for idr in [".git", "node_modules", "reversa/docs"]): continue
            for file in files:
                if file.endswith(".md"):
                    files_to_translate.append(Path(root) / file)
    
    print(f"📋 Found {len(files_to_translate)} markdown files to check.")
    for file_path in sorted(files_to_translate):
        translator.translate_file(file_path)

if __name__ == "__main__":
    main()

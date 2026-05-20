#!/usr/bin/env python3
import os
import sys

REPLACEMENTS = {
    "AXiomEngine": "AXiomEngine",
    "axiomengine": "axiomengine",
    "AXIOMENGINE": "AXIOMENGINE",
    "AXiom Engine": "AXiom Engine"
}

IGNORE_DIRS = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache", "logs", "cache", "docs/audit", "data/mission_archive"}
IGNORE_EXTS = {".pyc", ".png", ".jpg", ".zip", ".ext4", ".log"}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    original = content
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in IGNORE_EXTS:
                continue
            filepath = os.path.join(root, file)
            replace_in_file(filepath)

if __name__ == "__main__":
    main()

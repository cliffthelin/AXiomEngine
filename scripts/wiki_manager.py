#!/usr/bin/env python3
import os
from pathlib import Path
import datetime

WIKI_DIR = Path(__file__).parent.parent / "wiki"

class WikiManager:
    """
    Active Wiki Manager for AXiomEngine.
    Automates the generation and updating of internal documentation.
    """
    def __init__(self):
        WIKI_DIR.mkdir(exist_ok=True)

    def update_page(self, title: str, content: str):
        """Creates or updates a wiki page."""
        filename = f"{title.lower().replace(' ', '_')}.md"
        filepath = WIKI_DIR / filename
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        header = f"# {title}\n*Last Updated: {timestamp} by AXiomEngine Wiki Manager*\n\n"
        
        with open(filepath, "w") as f:
            f.write(header + content)
        
        print(f"WikiManager: Updated '{title}' at {filepath}")

if __name__ == "__main__":
    wm = WikiManager()
    wm.update_page("System Overview", "AXiomEngine is a multi-agent framework managed by Pi and Archon.")

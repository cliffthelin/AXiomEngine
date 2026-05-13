#!/usr/bin/env python3
import sys
import os
from typing import List, Dict, Any, Optional

class TUIFramework:
    def __init__(self):
        self.prev_lines: List[str] = []
        self.width = 80
        self.height = 24
        self.components = []
        self.focus_index = 0

    def start_sync_update(self):
        """CSI 2026 atomic update start."""
        sys.stdout.write("\x1b[?2026h")

    def end_sync_update(self):
        """CSI 2026 atomic update end."""
        sys.stdout.write("\x1b[?2026l")

    def render(self):
        """Differential rendering implementation."""
        self.start_sync_update()
        
        new_lines = []
        for comp in self.components:
            new_lines.extend(comp.render(self.width))
            
        # Differential logic
        for i, line in enumerate(new_lines):
            if i >= len(self.prev_lines) or line != self.prev_lines[i]:
                # Move cursor to line i, col 0
                sys.stdout.write(f"\x1b[{i+1};1H")
                # Clear line and write new content
                sys.stdout.write("\x1b[2K" + line)
        
        # Clear extra lines if new output is shorter
        if len(self.prev_lines) > len(new_lines):
            for i in range(len(new_lines), len(self.prev_lines)):
                sys.stdout.write(f"\x1b[{i+1};1H\x1b[2K")
                
        self.prev_lines = new_lines
        sys.stdout.flush()
        self.end_sync_update()

    def handle_input(self, data: str):
        if self.components:
            self.components[self.focus_index].handle_input(data)
            self.render()

class TUIComponent:
    def render(self, width: number) -> List[str]:
        return []
    def handle_input(self, data: str):
        pass

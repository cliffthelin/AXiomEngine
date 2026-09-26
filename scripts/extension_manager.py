#!/usr/bin/env python3
import os
import sys
import importlib.util
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional, Union
from scripts.agent_types import AgentTool
from scripts.pi_config import get_agent_dir

class ExtensionUI:
    """The 'ctx.ui' object for user interaction."""
    def __init__(self, tui=None):
        self.tui = tui

    async def confirm(self, title: str, message: str) -> bool:
        if self.tui:
            return await self.tui.confirm(title, message)
        print(f"[CONFIRM] {title}: {message} (y/n)")
        res = input(">> ")
        return res.lower() == 'y'

    async def input(self, prompt: str) -> str:
        if self.tui:
            return await self.tui.get_input(prompt)
        return input(f"{prompt} >> ")

    def notify(self, message: str, level: str = "info"):
        if self.tui:
            self.tui.notify(message, level)
        else:
            print(f"[{level.upper()}] {message}")

    def setStatus(self, ext_id: str, message: str):
        if self.tui:
            self.tui.status = message

    def setWidget(self, ext_id: str, lines: List[str]):
        if self.tui:
            # Simplified: add to a sidebar or specific area
            pass

class ExtensionAPI:
    def __init__(self, manager: 'ExtensionManager'):
        self.manager = manager
        self.registered_tools: List[AgentTool] = []
        self.registered_commands: Dict[str, Any] = {}
        self.registered_shortcuts: Dict[str, Callable] = {}
        self.registered_flags: Dict[str, Any] = {}
        self.registered_rule_providers: Dict[str, List[Callable]] = {}
        self.listeners: Dict[str, List[Callable]] = {}

    def registerTool(self, tool_def: Dict[str, Any]):
        tool = AgentTool(**tool_def)
        self.registered_tools.append(tool)

    def registerCommand(self, name: str, config: Any):
        if callable(config):
            self.registered_commands[name] = {"handler": config}
        else:
            self.registered_commands[name] = config

    def registerShortcut(self, key: str, handler: Callable):
        self.registered_shortcuts[key] = handler

    def registerFlag(self, name: str, config: Any):
        self.registered_flags[name] = config

    def registerRuleProvider(self, scope: str, handler: Callable):
        """PI Rule Extensions (Phase 7): let an extension contribute PDD rule
        content for a given scope. `handler()` (sync or async) must return a
        list of {rule_id, title, content} dicts. Providers are aggregated by
        `scripts/index_extension_rules.py`, which embeds and upserts them into
        `pdd_rules` so they flow through the existing rule-injection pipeline
        (`get_pdd_rules`) just like any other rule."""
        self.registered_rule_providers.setdefault(scope, []).append(handler)

    def on(self, event_name: str, handler: Callable):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(handler)

    async def emit(self, event_name: str, event_data: Any, context: Any = None):
        if event_name in self.listeners:
            for handler in self.listeners[event_name]:
                try:
                    if asyncio.iscoroutinefunction(handler):
                        await handler(event_data, context)
                    else:
                        handler(event_data, context)
                except Exception as e:
                    print(f"Extension Error in '{event_name}': {e}")

class ExtensionManager:
    def __init__(self):
        self.api = ExtensionAPI(self)
        self.extensions: List[Any] = []

    def discover_extensions(self, project_dir: str = "."):
        search_paths = [get_agent_dir() / "extensions", Path(project_dir) / ".pi" / "extensions"]
        
        # Add package paths
        pkg_paths = self._get_package_paths(project_dir)
        search_paths.extend([p / "extensions" for p in pkg_paths])
        
        for base_path in search_paths:
            if not base_path.exists(): continue
            for py_file in base_path.glob("*.py"): self.load_extension(py_file)
            for sub_dir in base_path.iterdir():
                if sub_dir.is_dir():
                    index_file = sub_dir / "index.py"
                    if index_file.exists(): self.load_extension(index_file)

    def _get_package_paths(self, project_dir: str) -> List[Path]:
        """Resolve package directories from settings."""
        paths = []
        # Simplified: Check ~/.pi/agent/git/ and .pi/git/ for now
        git_global = get_agent_dir() / "git"
        if git_global.exists():
            paths.extend([d for d in git_global.iterdir() if d.is_dir()])
        return paths

    async def collect_rules(self) -> List[Dict[str, Any]]:
        """Invoke every registered rule provider and return a flat list of
        {scope, rule_id, title, content} dicts contributed by extensions."""
        collected = []
        for scope, handlers in self.api.registered_rule_providers.items():
            for handler in handlers:
                try:
                    rules = await handler() if asyncio.iscoroutinefunction(handler) else handler()
                except Exception as e:
                    print(f"Extension rule provider error (scope={scope}): {e}")
                    continue
                for rule in rules or []:
                    collected.append({
                        "scope": scope,
                        "rule_id": rule["rule_id"],
                        "title": rule.get("title"),
                        "content": rule["content"],
                    })
        return collected

    def load_extension(self, path: Path):
        try:
            spec = importlib.util.spec_from_file_location(path.stem, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "default"): module.default(self.api)
            elif hasattr(module, "setup"): module.setup(self.api)
            self.extensions.append(module)
        except Exception as e:
            print(f"Failed to load extension {path}: {e}")

_manager = None
def get_manager():
    global _manager
    if _manager is None:
        _manager = ExtensionManager()
    return _manager

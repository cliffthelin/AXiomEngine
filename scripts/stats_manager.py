#!/usr/bin/env python3
import json
from typing import Dict, Any, List
from scripts.pi_config import get_agent_dir

class StatsManager:
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0.0

    def record_usage(self, model: str, input_tokens: int, output_tokens: int):
        # Pricing table (simplified)
        pricing = {
            "claude-3-5-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
            "gpt-4o": {"input": 0.005 / 1000, "output": 0.015 / 1000},
            "qwen3.6": {"input": 0.0, "output": 0.0} # Local
        }
        
        rates = pricing.get(model, {"input": 0.0, "output": 0.0})
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])
        
        self.total_tokens += (input_tokens + output_tokens)
        self.total_cost += cost
        
    def get_summary(self):
        return {
            "total_tokens": self.total_tokens,
            "total_cost": self.total_cost,
            "currency": "USD"
        }

_manager = None
def get_stats_manager():
    global _manager
    if _manager is None:
        _manager = StatsManager()
    return _manager

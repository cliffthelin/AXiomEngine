import time
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class TurnMetrics:
    turn_id: str
    mode: str # websocket or http
    ttft: float = 0.0 # Time to first token
    total_latency: float = 0.0
    tool_latency: float = 0.0
    context_render_latency: float = 0.0
    cache_hit: bool = False
    tokens_reused: int = 0

class AgentLatencyMetrics:
    """
    AXIOMENGINE PERFORMANCE INSTRUMENTATION
    Records and benchmarks agent loop performance.
    """
    def __init__(self):
        self.turns: List[TurnMetrics] = []

    def record_turn(self, metrics: TurnMetrics):
        self.turns.append(metrics)

    def generate_report(self):
        if not self.turns:
            return "No metrics recorded."

        ws_turns = [t for t in self.turns if t.mode == "websocket"]
        http_turns = [t for t in self.turns if t.mode == "http"]

        report = "=== Agent Latency Benchmark ===\n"
        if ws_turns:
            avg_ws = sum(t.total_latency for t in ws_turns) / len(ws_turns)
            report += f"WebSocket Avg Latency: {avg_ws:.2f}ms\n"
        
        if http_turns:
            avg_http = sum(t.total_latency for t in http_turns) / len(http_turns)
            report += f"HTTP Avg Latency: {avg_http:.2f}ms\n"

        if ws_turns and http_turns:
            improvement = (1 - (avg_ws / avg_http)) * 100
            report += f"Realtime Improvement: {improvement:.1f}%\n"
        
        return report

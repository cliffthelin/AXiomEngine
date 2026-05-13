import asyncio
import time
import uuid
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.transport.transport_selector import TransportSelector
from core.metrics.agent_latency_metrics import AgentLatencyMetrics, TurnMetrics

async def run_benchmark(mode="http", turns=3):
    print(f"\n🚀 Running {mode.upper()} Benchmark ({turns} turns)...")
    
    ws_uri = "ws://localhost:9001/v1/realtime"
    http_url = "http://localhost:9001"
    
    selector = TransportSelector(ws_uri, http_url)
    metrics = AgentLatencyMetrics()
    session_id = f"bench-{mode}-{uuid.uuid4().hex[:6]}"
    
    # Force mode for benchmark
    if mode == "websocket":
        await selector.initialize()
    else:
        selector.active_mode = "http"

    headers = {"X-Session-Id": session_id, "X-Agent-Name": "Benchmark"}
    
    for i in range(turns):
        t_start = time.monotonic()
        payload = {
            "model": "nemotron",
            "messages": [{"role": "user", "content": f"Turn {i+1}: What is the current system time?"}]
        }
        
        # Simulate turn
        res = await selector.send_turn(payload, headers=headers)
        
        latency = (time.monotonic() - t_start) * 1000
        metrics.record_turn(TurnMetrics(
            turn_id=f"{session_id}-{i}",
            mode=selector.active_mode,
            total_latency=latency,
            cache_hit=(i > 0 and selector.active_mode == "websocket")
        ))
        print(f"  [Turn {i+1}] Latency: {latency:.2f}ms (Mode: {selector.active_mode})")
        
    return metrics

async def main():
    print("=== AXiomEngine Realtime Benchmark Suite ===")
    
    # 1. Warm up & HTTP baseline
    http_metrics = await run_benchmark(mode="http", turns=3)
    
    # 2. WebSocket optimized run
    ws_metrics = await run_benchmark(mode="websocket", turns=3)
    
    # 3. Final Report
    full_metrics = AgentLatencyMetrics()
    full_metrics.turns = http_metrics.turns + ws_metrics.turns
    print("\n" + full_metrics.generate_report())

if __name__ == "__main__":
    asyncio.run(main())

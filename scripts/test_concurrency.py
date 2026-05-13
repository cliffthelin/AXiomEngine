#!/usr/bin/env python3
import asyncio
import httpx
import time

ROUTER_URL = "http://127.0.0.1:9001/v1/chat/completions"

async def send_request(client, task_id):
    start = time.monotonic()
    payload = {
        "model": "nemotron",
        "messages": [{"role": "user", "content": f"Task {task_id}: Explain PDD rule R-PDD-CORE-002."}],
        "stream": false
    }
    try:
        resp = await client.post(ROUTER_URL, json=payload, timeout=120.0)
        latency = int((time.monotonic() - start) * 1000)
        print(f"[Task {task_id}] Status: {resp.status_code} | Latency: {latency}ms")
    except Exception as e:
        print(f"[Task {task_id}] Error: {e}")

async def run_test(num_requests=5):
    print(f"── Test Scenario 2: Concurrency Load (n={num_requests}) ──")
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, i) for i in range(num_requests)]
        await asyncio.gather(*tasks)
    print("────────────────────────────────────────────────────────")

if __name__ == "__main__":
    asyncio.run(run_test())

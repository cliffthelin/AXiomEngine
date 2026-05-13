# AXiomEngine: WebSocket Agent Loop Optimization

## Overview
This document describes the high-performance, realtime agent loop implemented in AXiomEngine. This architecture is designed to reduce end-to-end latency in multi-turn agentic workflows by replacing stateless HTTP request/response cycles with a persistent, session-aware WebSocket transport.

## Key Features

### 1. Persistent Session Layer (`AgentSession`)
- **Conversation Rehydration**: Instead of re-sending the entire history on every turn, the agent only sends the "delta" (the most recent message or tool result). The Router rehydrates the full context from its local `ResponseStateCache`.
- **State Survival**: The session survives across tool executions, allowing for a continuous sampling loop.

### 2. Dual Transport Strategy
- **WebSocket (Primary)**: Provides full-duplex communication for real-time tool pause/resume events.
- **HTTP (Fallback)**: Automatically engaged if the WebSocket connection drops or is unavailable, ensuring workflow continuity without correctness loss.

### 3. Tool Pause & Resume
- **Local Tool Execution**: When the model triggers a tool, the harness pauses the sampling loop, executes the tool in the local sandbox, and resumes the inference over the same persistent channel.
- **Zero-History Replay**: By reusing the cached KVP state, the system avoids the quadratic cost of re-processing large histories after every tool call.

## Governance Rules (R-PDD-REALTIME-001)
1. **Session Integrity**: A session must only be rehydrated if the `session_id` and `connection_id` match.
2. **Safety Re-validation**: Incremental deltas must still pass through the PDD safety filters before being appended to the cached context.
3. **Resource Quotas**: Persistent sessions are subject to TTL (default 1 hour) and VRAM reservation quotas.

## Performance Targets
- **End-to-End Latency**: Target ~40% reduction for workflows involving 3+ tool calls.
- **TTFT (Time to First Token)**: Reduced by avoiding full-history tokenization on the backend.

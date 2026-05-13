# Mode 1 — Split LLM Inference
// RULE-START: R-PDD-MD-001
# R-PDD-MD-001: This document is the authoritative definition of Mode 1.
// RULE-END: R-PDD-MD-001

## Purpose and Scope
Defines the hardware allocation, startup parameters, and operational constraints
for Mode 1: split-GPU LLM inference across the Tesla P40 and RTX 3070.

## Hardware Allocation
| GPU | Index | VRAM | Role |
|---|---|---|---|
| Tesla P40 | GPU 1 (nvidia-smi) | 24 GB | Model body (majority of layers) |
| RTX 3070 | GPU 0 (nvidia-smi) | 8 GB | Model head + KV cache |
| AMD Raphael | — | shared | Display ONLY (no AI) |

## Current Model
**nemotron-3-nano (snap)** — Nemotron-Nano-3-30B-A3B-Q4_K_M
- Snap name: `nemotron-3-nano`
- Port: 8080 (localhost only)
- Auto-split: managed by snap
- Endpoint: `http://127.0.0.1:8080/v1/chat/completions`

## Manual llama.cpp Split (for custom models)
```bash
# Build llama.cpp with CUDA (Pascal=60, Ampere=86)
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES="60;86"
cmake --build build -j16

# Run with P40=3 parts, 3070=1 part (proportional to 24GB:8GB)
./build/bin/llama-server \
  -m /path/to/model.gguf \
  --n-gpu-layers 999 \
  --tensor-split 3,1 \
  --main-gpu 1 \     # P40 is index 1
  --ctx-size 32768 \
  --host 127.0.0.1 --port 8081
```

## VRAM Budget
| Model | Q4_K_M | P40 usage | 3070 usage | Max ctx |
|---|---|---|---|---|
| Gemma 4 9B | ~6 GB | all on P40 | 0 | 128K |
| Nemotron 30B | ~20 GB | ~15 GB | ~5 GB | 32K |
| Qwen 3 30B | ~21 GB | ~16 GB | ~5 GB | 32K |
| Qwen 3 72B | ~50 GB | DOES NOT FIT | — | route to API |
// RULE-START: R-MODE1-001
// RULE-START: R-MODE1-002

// RULE-END: R-MODE1-002
// RULE-END: R-MODE1-001
// RULE-START: R-MODE1-004
// RULE-START: R-MODE1-004
// RULE-END: R-MODE1-004
## Constraints (Authoritative)
// RULE-END: R-MODE1-004
// RULE-START: R-MODE1-003
- R-MODE1-001: P40 temp MUST NOT exceed 85°C under sustained load
// RULE-END: R-MODE1-003
- R-MODE1-002: Display output MUST use AMD Raphael iGPU in this mode
- R-MODE1-003: Context size MUST NOT exceed 32768 tokens without explicit override
- R-MODE1-004: All requests MUST route through AXiomEngine Router (port 9001) for audit

## Validation
- ✅ `nvidia-smi` shows both GPUs allocated
- ✅ `curl http://127.0.0.1:8080/health` returns `{"status":true}`
- ✅ `curl http://127.0.0.1:9001/health` returns router status

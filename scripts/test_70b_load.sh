#!/usr/bin/env bash
# =============================================================================
# Test Scenario 1: 70B Model Overspill Test
# Target: Kimiko-V2-70B (37GB) -> 32GB VRAM + 5GB RAM
# =============================================================================
set -euo pipefail

MODEL="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Models/TheBloke/fiction.live-Kimiko-V2-70B-GGUF/fiction.live-Kimiko-V2-70B.Q4_K_S.gguf"
LLAMA_BIN="/snap/nemotron-3-nano/components/mnt/llama-cpp-cuda/36/bin/llama-server"

echo "── Test Scenario 1: 70B Split Load ────────────────"
echo "  Model:  $(basename "$MODEL")"
echo "  Total VRAM: 32 GB (8GB 3070 + 24GB P40)"
echo "  Model Size: 37 GB"
echo "  Expected Overspill: ~5 GB into System RAM"
echo "────────────────────────────────────────────────────"

# Ensure other AI services are stopped to free VRAM
echo "  Stopping conflicting services..."
snap stop nemotron-3-nano 2>/dev/null || true
pkill -f "llama-server" 2>/dev/null || true

# Start the 70B load
# Split ratio 1:3 (3070=1 part, P40=3 parts)
# Main GPU = 1 (P40 has more room for KV cache)
echo "  Starting llama-server on port 8090..."
export LD_LIBRARY_PATH="/snap/nemotron-3-nano/components/mnt/llama-cpp-cuda/36/lib:$LD_LIBRARY_PATH"
"$LLAMA_BIN" \
    -m "$MODEL" \
    --n-gpu-layers 999 \
    --tensor-split 1,3 \
    --main-gpu 1 \
    --ctx-size 8192 \
    --port 8090 \
    --host 127.0.0.1 \
    --no-warmup 2>&1 | tee /tmp/test_70b.log &

TEST_PID=$!
echo "  Server PID: $TEST_PID"
echo "  Monitoring load... (Check /tmp/test_70b.log for progress)"

# Poll for "all layers offloaded" or memory status
sleep 10
nvidia-smi
free -h

echo "────────────────────────────────────────────────────"
echo "  Test is running. You can query it via:"
echo "  curl http://127.0.0.1:8090/health"
echo "────────────────────────────────────────────────────"

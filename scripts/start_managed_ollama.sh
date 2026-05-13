#!/usr/bin/env bash
# Managed Ollama Launcher for AXiomEngine
# Starts two instances: 11436 (3070) and 11437 (P40)

OLLAMA_BIN="/tmp/ollama_dist/bin/ollama"
LOG_DIR="/mnt/UBUNTU_8TB/Projects/axiomengine/logs"
mkdir -p "$LOG_DIR"

# Kill existing cane-owned ollama serve
pkill -u "$USER" -f "ollama serve" || true
sleep 2

echo "🚀 Starting Ollama Instance 11436 (RTX 3070)..."
OLLAMA_HOST=127.0.0.1:11436 \
CUDA_VISIBLE_DEVICES=0 \
"$OLLAMA_BIN" serve >> "$LOG_DIR/ollama_3070_managed.log" 2>&1 &

echo "🚀 Starting Ollama Instance 11437 (Tesla P40)..."
OLLAMA_HOST=127.0.0.1:11437 \
CUDA_VISIBLE_DEVICES=1 \
"$OLLAMA_BIN" serve >> "$LOG_DIR/ollama_p40_managed.log" 2>&1 &

sleep 5
echo "✅ Ollama instances launched."

#!/usr/bin/env bash
set -euo pipefail
# Managed Ollama Launcher for AXiomEngine
# Starts two additional governed instances:
#   11436 -> RTX 3070 researcher/skill lanes
#   11437 -> Tesla P40 architect lane

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OLLAMA_BIN="${OLLAMA_BIN:-$(command -v ollama || true)}"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

if [[ -z "$OLLAMA_BIN" || ! -x "$OLLAMA_BIN" ]]; then
  echo "ERROR: ollama executable not found. Set OLLAMA_BIN=/path/to/ollama." >&2
  exit 1
fi

start_lane() {
  local port="$1"
  local gpu="$2"
  local name="$3"
  local log_file="$LOG_DIR/ollama_${name}_managed.log"

  if curl -fsS --max-time 1 "http://127.0.0.1:${port}/api/tags" >/dev/null 2>&1; then
    echo "✅ Ollama ${name} lane already listening on ${port}."
    return 0
  fi

  echo "🚀 Starting Ollama ${name} lane on ${port} (CUDA_VISIBLE_DEVICES=${gpu})..."
  OLLAMA_HOST="127.0.0.1:${port}" \
  CUDA_VISIBLE_DEVICES="${gpu}" \
  "$OLLAMA_BIN" serve >> "$log_file" 2>&1 &
}

start_lane 11436 0 "rtx3070"
start_lane 11437 1 "p40"

sleep 5
for port in 11436 11437; do
  if curl -fsS --max-time 2 "http://127.0.0.1:${port}/api/tags" >/dev/null; then
    echo "✅ Port ${port} ready."
  else
    echo "⚠️ Port ${port} did not become ready. Check $LOG_DIR/ollama_*_managed.log" >&2
  fi
done

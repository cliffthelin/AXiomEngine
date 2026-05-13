#!/usr/bin/env bash
# =============================================================================
# MODE SWITCHER — Switch between the 4 operational modes
# Usage:  bash switch_mode.sh [1|2|3|4|gaming]
# =============================================================================
set -euo pipefail

MODE="${1:-}"
if [ -z "$MODE" ]; then
    echo "Usage: $0 [1|2|3|4|gaming]"
    echo ""
    echo "  1 / split  — Split LLM (P40 body + 3070 head) — AI agents"
    echo "  2 / comfy  — ComfyUI image/video (P40 UNet + 3070 VAE)"
    echo "  3 / direct — Direct model → single card"
    echo "  4 / gaming — Gaming (3070 primary display + render)"
    exit 1
fi

echo "── Mode Switch: $MODE ──────────────────────────────"

case "$MODE" in
    1|split|llm)
        echo "→ Mode 1: Split LLM Inference"
        # Notify router
        curl -sf -X POST http://127.0.0.1:9001/admin/mode/split 2>/dev/null && echo "  ✅ Router updated" || echo "  ⚠️  Router not running"
        # Ensure nemotron snap is running
        snap start nemotron-3-nano 2>/dev/null || true
        # Ensure display is on Raphael if possible
        echo "  📌 Reminder: Verify display on AMD Raphael iGPU"
        ;;

    2|comfy|comfyui)
        echo "→ Mode 2: ComfyUI Image/Video Generation"
        curl -sf -X POST http://127.0.0.1:9001/admin/mode/split 2>/dev/null || true
        COMFY_DIR="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/ComfyUI"
        if [ -d "$COMFY_DIR" ]; then
            echo "  Starting ComfyUI..."
            cd "$COMFY_DIR"
            # P40 (index 1) = primary compute, 3070 (index 0) = VAE/CLIP
            CUDA_VISIBLE_DEVICES=1,0 python main.py \
                --cuda-device 0 \
                --listen 0.0.0.0 \
                --port 8188 &
            echo "  ✅ ComfyUI starting on :8188 (PID: $!)"
        else
            echo "  ⚠️  ComfyUI not found at $COMFY_DIR"
            echo "  Install: git clone https://github.com/comfyanonymous/ComfyUI $COMFY_DIR"
        fi
        ;;

    3|direct|p40)
        echo "→ Mode 3: Direct Model Delegation"
        MODEL="${2:-}"
        CARD="${3:-p40}"
        if [ -z "$MODEL" ]; then
            echo "  Usage: $0 3 <model.gguf> [p40|3070]"
            exit 1
        fi
        GPU_IDX=1  # P40 default
        PORT=8081
        [ "$CARD" = "3070" ] && GPU_IDX=0 && PORT=8082
        LLAMA_BIN="/mnt/usb.../llama.cpp/build/bin/llama-server"
        echo "  Starting $MODEL on GPU $GPU_IDX (port $PORT)..."
        CUDA_VISIBLE_DEVICES=$GPU_IDX "$LLAMA_BIN" \
            -m "$MODEL" \
            --n-gpu-layers 999 \
            --port "$PORT" \
            --host 127.0.0.1 &
        echo "  ✅ Model on card $CARD, port $PORT (PID: $!)"
        ;;

    4|gaming)
        echo "→ Mode 4: Gaming"
        echo "  Stopping AI services to free RTX 3070..."
        snap stop nemotron-3-nano 2>/dev/null && echo "  ✅ Nemotron stopped" || true
        kill $(pgrep -f "comfyui" 2>/dev/null) 2>/dev/null || true
        
        echo "  Setting P40 to EXCLUSIVE_COMPUTE (shader cache mode)..."
        sudo nvidia-smi -i 1 -c EXCLUSIVE_COMPUTE 2>/dev/null || true
        
        echo "  Configuring 3070 as primary display..."
        # This requires a display restart - warn the user
        cat << 'MSG'

  ┌─────────────────────────────────────────────────────────┐
  │  GAMING MODE REQUIRES DISPLAY SWITCH                    │
  │                                                         │
  │  Connect monitor to RTX 3070 port (if using Raphael)   │
  │  Then log out and back in to switch display adapters    │
  │                                                         │
  │  GPU 1 (P40) is now in EXCLUSIVE_COMPUTE mode          │
  │  for shader pre-compilation assistance                  │
  └─────────────────────────────────────────────────────────┘
MSG
        ;;
    *)
        echo "Unknown mode: $MODE"
        exit 1
        ;;
esac

echo "── Done ────────────────────────────────────────────"

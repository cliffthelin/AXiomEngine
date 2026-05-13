#!/usr/bin/env bash
# =============================================================================
# AXIOMENGINE GOVERNANCE RECOVERY: Full GPU/Ollama Reset
# Run with: sudo ./RECOVERY_RESET.sh
# =============================================================================

echo "🛑 Stopping all Ollama services..."
systemctl stop ollama || true
pkill -9 ollama || true
pkill -9 llama-server || true

echo "🔄 Resetting NVIDIA Driver State..."
modprobe -r nvidia_uvm || true
modprobe -r nvidia_drm || true
modprobe -r nvidia_modeset || true
modprobe -r nvidia || true

echo "🔋 Reloading NVIDIA Modules..."
modprobe nvidia
modprobe nvidia_modeset
modprobe nvidia_drm
modprobe nvidia_uvm

echo "✅ Verifying Hardware..."
nvidia-smi -L

echo "🚀 Restarting Ollama..."
systemctl start ollama

echo "🐝 The Swarm will automatically detect the recovery and move back to GPU."

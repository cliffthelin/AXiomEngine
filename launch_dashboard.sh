#!/usr/bin/env bash
# AXiomEngine Dashboard Launcher
# Ensures the correct venv and PYTHONPATH are used.

VENV_PYTHON="/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/.agentos_venv/bin/python3"
PROJECT_ROOT="/mnt/UBUNTU_8TB/Projects/agentos"

if [[ ! -f "$VENV_PYTHON" ]]; then
    echo "❌ Error: Virtual environment not found at $VENV_PYTHON"
    exit 1
fi

cd "$PROJECT_ROOT"
export PYTHONPATH=$PYTHONPATH:.

echo "🏛️  Starting AXiomEngine C2 Dashboard Server..."
"$VENV_PYTHON" scripts/governance_dashboard_server.py --port 8765

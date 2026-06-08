#!/usr/bin/env bash
# AXiomEngine Dashboard Launcher
# Keeps the venv outside the repo by default so the project folder stays portable.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${AGENTOS_VENV:-$HOME/.agentos_venv}"
VENV_PYTHON="$VENV/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "Error: virtual environment not found at $VENV"
    echo "Create it with: python3 -m venv \"$VENV\" && \"$VENV/bin/pip\" install -r \"$PROJECT_ROOT/requirements.txt\""
    exit 1
fi

cd "$PROJECT_ROOT"
export PYTHONPATH="${PYTHONPATH:-}:."

PORT="${1:-8765}"

# If the preferred port is already occupied (e.g., by a system service on boot),
# try the next port automatically rather than failing.
if ss -tlnH sport = :"$PORT" 2>/dev/null | grep -q .; then
    EXISTING_PID=$(lsof -t -i :"$PORT" 2>/dev/null || fuser "$PORT"/tcp 2>/dev/null || true)
    EXISTING_CMD=""
    if [[ -n "$EXISTING_PID" ]]; then
        EXISTING_CMD=$(ps -p "$EXISTING_PID" -o args= 2>/dev/null || true)
    fi
    if [[ "$EXISTING_CMD" == *"governance_dashboard_server"* ]]; then
        echo "Stopping existing dashboard (PID $EXISTING_PID) on port $PORT..."
        kill "$EXISTING_PID" 2>/dev/null || true
        sleep 2
        kill -0 "$EXISTING_PID" 2>/dev/null && kill -9 "$EXISTING_PID" 2>/dev/null
        sleep 1
    else
        # Port held by something else — try next port
        echo "Port $PORT is in use (PID: ${EXISTING_PID:-unknown}). Trying port $((PORT+1))..."
        PORT=$((PORT+1))
    fi
fi

echo "Starting AXiomEngine C2 Dashboard Server with $VENV_PYTHON on port $PORT..."

# Start PI Web Bridge (serves TUI terminal at :8770) if not already running
if ! curl -sf --max-time 1 http://127.0.0.1:8770/health &>/dev/null; then
    echo "Starting PI Web Bridge on port 8770..."
    "$VENV_PYTHON" scripts/pi_web_bridge.py --port 8770 &>/dev/null & disown
    sleep 1
fi

"$VENV_PYTHON" scripts/governance_dashboard_server.py --port "$PORT"

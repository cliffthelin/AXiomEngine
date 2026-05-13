#!/usr/bin/env bash
# Archon Architect Launcher
# Starts the Archon agent for planning and governance.

VENV="$HOME/.axiomengine_venv"

if [ -f "$VENV/bin/python" ]; then
    PYTHON="$VENV/bin/python"
else
    echo "Warning: AXiomEngine Venv not found. Trying system python."
    PYTHON="python3"
fi

exec "$PYTHON" archon/archon.py "$@"

#!/usr/bin/env bash
# PI Agent Launcher
# Opens the PI TUI (Personal Intelligence).

VENV="$HOME/.axiomengine_venv"
OTHER_VENV="/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/.axiomengine_venv"

if [ -f "$VENV/bin/python" ] && [ -d "$VENV/lib/python3.14/site-packages" ]; then
    PYTHON="$VENV/bin/python"
elif [ -d "$OTHER_VENV/lib/python3.14/site-packages" ]; then
    PYTHON="python3"
    export PYTHONPATH="$OTHER_VENV/lib/python3.14/site-packages"
    echo "Using fallback venv from other OS drive."
else
    echo "Warning: AXiomEngine Venv not found. Trying system python."
    PYTHON="python3"
fi

exec "$PYTHON" pi/pi_tui.py "$@"

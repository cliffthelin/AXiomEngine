#!/usr/bin/env bash
# Hermes Agent Launcher
# Runs Hermes from the secondary OS mount.
HERMES_DIR="/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/hermes-agent"
VENV="$HERMES_DIR/venv"

if [ ! -d "$HERMES_DIR" ]; then
    echo "Error: Hermes directory not found. Is the drive mounted?"
    exit 1
fi

# The other OS drive has absolute symlinks that expect to be at /
# We need to map them to our current mount point.
OTHER_OS_ROOT="/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088"
OTHER_PYTHON="$OTHER_OS_ROOT/home/cane/.local/share/uv/python/cpython-3.11.15-linux-x86_64-gnu/bin/python3.11"

cd "$HERMES_DIR"
if [ -f "$OTHER_PYTHON" ]; then
    # We must set PYTHONPATH to include the venv's site-packages
    # because the other OS's python won't find them automatically
    # if it's not running from the expected prefix.
    export PYTHONPATH="$VENV/lib/python3.11/site-packages"
    exec "$OTHER_PYTHON" hermes "$@"
else
    # Fallback to system python if other OS python is not found
    exec python3 hermes "$@"
fi

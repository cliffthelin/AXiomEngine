#!/usr/bin/env bash
# Reversa Orchestrator
# Runs Reversa skills within the AXiomEngine environment.

OTHER_OS_ROOT="/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088"
OTHER_PYTHON="$OTHER_OS_ROOT/usr/bin/python3.14"
OTHER_VENV="$OTHER_OS_ROOT/home/cane/.axiomengine_venv"

if [ -f "$OTHER_PYTHON" ] && [ -d "$OTHER_VENV/lib/python3.14/site-packages" ]; then
    export PYTHONPATH="$OTHER_VENV/lib/python3.14/site-packages"
    exec "$OTHER_PYTHON" scripts/reversa_runner.py "$@"
else
    # Fallback to system python
    python3 scripts/reversa_runner.py "$@"
fi

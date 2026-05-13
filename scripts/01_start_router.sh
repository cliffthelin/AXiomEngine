#!/usr/bin/env bash
# =============================================================================
# Start AXiomEngine Router
# Run from: /Projects/axiomengine/
# =============================================================================
set -euo pipefail

# Use the directory where the script is located (go up one level from scripts/)
AXIOMENGINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$HOME/.axiomengine_venv"

echo "── AXiomEngine Router ────────────────────────────────"
echo "  Project: $AXIOMENGINE"

# Check venv exists
if [ ! -f "$VENV/bin/python" ]; then
    echo "Venv not found — creating $VENV..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install fastapi uvicorn httpx asyncpg "valkey>=6.0" pydantic numpy -q
fi

# Verify backends
echo "── Backend Health ────────────────────────────────"
for port in 8330 11434; do
    if curl -sf "http://127.0.0.1:$port/health" &>/dev/null || \
       curl -sf "http://127.0.0.1:$port/" &>/dev/null; then
        echo "  ✅ Port $port: UP"
    else
        echo "  ⚠️  Port $port: DOWN"
    fi
done

# Check Valkey
if command -v valkey-cli &>/dev/null && valkey-cli ping &>/dev/null; then
    echo "  ✅ Valkey: UP"
elif command -v redis-cli &>/dev/null && redis-cli ping &>/dev/null; then
    echo "  ✅ Redis (Valkey-compat): UP"
else
    echo "  ⚠️  Valkey: DOWN (run 00_install_base.sh)"
fi

# Check Postgres
if command -v pg_isready &>/dev/null && pg_isready -q; then
    echo "  ✅ Postgres: UP"
else
    echo "  ⚠️  Postgres: DOWN"
fi

echo "── Starting Router on :9001 ──────────────────────"
cd "$AXIOMENGINE/router"
exec "$VENV/bin/python" -m uvicorn main:app \
    --host 0.0.0.0 \
    --port 9001 \
    --reload \
    --log-level info

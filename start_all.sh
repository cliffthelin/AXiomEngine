#!/usr/bin/env bash
# =============================================================================
# AXiomEngine All-in-One Service Launcher & Controller (Resilient Ports)
# =============================================================================
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"
mkdir -p logs

# Color tokens
RESET='\033[0m'; BOLD='\033[1m'; GREEN='\033[0;32m'
YELLOW='\033[0;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'

ok()   { echo -e "${GREEN}[+] $*${RESET}"; }
warn() { echo -e "${YELLOW}[!] $*${RESET}"; }
fail() { echo -e "${RED}[x] $*${RESET}"; }
info() { echo -e "${CYAN}[i] $*${RESET}"; }
hdr()  { echo -e "\n${BOLD}${CYAN}=== $* ===${RESET}"; }

VENV="${AGENTOS_VENV:-$HOME/.agentos_venv}"

hdr "AXiomEngine Startup Sequence"

# Helper Functions
is_port_in_use() {
    local port="$1"
    if (echo > /dev/tcp/127.0.0.1/"$port") >/dev/null 2>&1; then
        return 0 # In use
    elif command -v nc &>/dev/null && nc -z 127.0.0.1 "$port" &>/dev/null; then
        return 0 # In use
    elif command -v ss &>/dev/null && ss -lptn | grep -q ":$port " 2>/dev/null; then
        return 0 # In use
    fi
    return 1 # Free
}

get_pid_on_port() {
    local port="$1"
    # Extract numeric PIDs from lsof or fuser, split by space/newline
    (lsof -t -i :"$port" 2>/dev/null || fuser "$port"/tcp 2>/dev/null || true) | tr ' ' '\n' | grep -v '^$' || true
}

get_process_app_type() {
    local pid="$1"
    if [ -z "$pid" ]; then
        echo "none"
        return
    fi
    local cmd
    cmd=$(ps -p "$pid" -o args= 2>/dev/null || true)
    if [[ "$cmd" == *"uvicorn"* || "$cmd" == *"router"* || "$cmd" == *"main:app"* ]]; then
        echo "router"
    elif [[ "$cmd" == *"governance_dashboard_server.py"* ]]; then
        echo "dashboard"
    else
        echo "other"
    fi
}

check_router_health() {
    local port="$1"
    local resp
    resp=$(curl -sf --max-time 2 "http://127.0.0.1:${port}/health" 2>/dev/null || true)
    if [[ "$resp" == *"postgres"* && "$resp" == *"valkey"* ]]; then
        echo "healthy"
    else
        echo "unhealthy"
    fi
}

check_dashboard_health() {
    local port="$1"
    local resp
    resp=$(curl -sf --max-time 2 "http://127.0.0.1:${port}/health" 2>/dev/null || true)
    if [[ "$resp" == *"project_root"* && "$resp" == *"version"* ]]; then
        echo "healthy"
    else
        echo "unhealthy"
    fi
}

kill_process() {
    local pid="$1"
    info "Killing process $pid..."
    kill "$pid" 2>/dev/null || true
    sleep 1.5
    if kill -0 "$pid" 2>/dev/null; then
        warn "Process $pid refused to terminate. Force killing..."
        kill -9 "$pid" 2>/dev/null || true
        sleep 1
    fi
}

find_available_port() {
    local start_port="$1"
    local port="$start_port"
    while true; do
        if ! is_port_in_use "$port"; then
            echo "$port"
            return 0
        fi
        port=$((port + 1))
    done
}

# 1. Valkey Cache Server
hdr "1. Checking Valkey / Redis Cache"
VALKEY_RUNNING=0
if command -v valkey-cli &>/dev/null && valkey-cli ping &>/dev/null 2>&1; then
    ok "Valkey is already running on port 6379."
    VALKEY_RUNNING=1
elif command -v redis-cli &>/dev/null && redis-cli ping &>/dev/null 2>&1; then
    ok "Redis (Valkey-compatible) is already running on port 6379."
    VALKEY_RUNNING=1
fi

if [ $VALKEY_RUNNING -eq 0 ]; then
    info "Valkey is down. Attempting to start local Valkey..."
    if [ -f "valkey_local.conf" ]; then
        if command -v valkey-server &>/dev/null; then
            valkey-server valkey_local.conf
            ok "Valkey server started using local config."
        elif command -v redis-server &>/dev/null; then
            redis-server valkey_local.conf
            ok "Redis server started using local config."
        else
            fail "Neither valkey-server nor redis-server binary found in PATH."
        fi
    else
        fail "Local configuration valkey_local.conf not found."
    fi
    sleep 1
fi

# 2. Postgres Database
hdr "2. Checking Postgres Database"
PG_RUNNING=0
for port in 5433 5432; do
    if pg_isready -p "$port" -q 2>/dev/null; then
        ok "PostgreSQL is active on port $port."
        PG_RUNNING=1
        break
    fi
done

if [ $PG_RUNNING -eq 0 ]; then
    warn "PostgreSQL is down on ports 5432 and 5433."
    info "Attempting to start PostgreSQL service..."
    if command -v systemctl &>/dev/null; then
        sudo systemctl start postgresql || warn "Failed to start postgresql via systemctl without root. Please ensure database is running."
    else
        warn "systemctl not found. Please ensure Postgres service is running."
    fi
    sleep 2
    # recheck
    for port in 5433 5432; do
        if pg_isready -p "$port" -q 2>/dev/null; then
            ok "PostgreSQL successfully started/running on port $port."
            PG_RUNNING=1
            break
        fi
    done
    if [ $PG_RUNNING -eq 0 ]; then
        fail "PostgreSQL is still DOWN. Core engine tables and stats queries might fail!"
    fi
fi

# 3. Ollama LLM Lanes
hdr "3. Checking Ollama Inference Lanes"
if curl -sf --max-time 1 "http://127.0.0.1:11434/api/tags" &>/dev/null; then
    ok "Ollama default lane active on port 11434."
else
    info "Default Ollama instance down. Starting 'ollama serve'..."
    if command -v ollama &>/dev/null; then
        nohup ollama serve > logs/ollama_default.log 2>&1 &
        ok "Ollama default daemon started in background (port 11434)."
    else
        fail "ollama executable not found. Cannot start default lane."
    fi
fi

# Multi-GPU Lanes (11436 / 11437)
info "Checking managed GPU lanes..."
if [ -f "scripts/start_managed_ollama.sh" ]; then
    bash scripts/start_managed_ollama.sh
else
    warn "scripts/start_managed_ollama.sh not found."
fi

# 4. AXiomEngine Router
hdr "4. Launching AXiomEngine Router"
ROUTER_PORT=9001

start_router() {
    local port="$1"
    info "Starting Router on port $port..."
    (
        cd "$PROJECT_ROOT/router"
        export PYTHONPATH="${PYTHONPATH:-}:.."
        nohup "$VENV/bin/python" -m uvicorn main:app \
            --host 0.0.0.0 \
            --port "$port" \
            --log-level info > "$PROJECT_ROOT/logs/router.log" 2>&1 &
    )
    info "Waiting for Router to initialize..."
    sleep 3
    local check
    check=$(check_router_health "$port")
    if [ "$check" = "healthy" ]; then
        ok "AXiomEngine Router successfully active on port $port."
    else
        warn "Router started but port $port is not responding healthy yet. Check logs/router.log"
    fi
}

if is_port_in_use $ROUTER_PORT; then
    PIDS_ROUTER=$(get_pid_on_port $ROUTER_PORT)
    IS_OUR_APP=0
    PID_TO_MANAGE=""
    for pid in $PIDS_ROUTER; do
        if [ "$(get_process_app_type "$pid")" = "router" ]; then
            IS_OUR_APP=1
            PID_TO_MANAGE="$pid"
            break
        fi
    done

    if [ $IS_OUR_APP -eq 1 ]; then
        HEALTH=$(check_router_health $ROUTER_PORT)
        if [ "$HEALTH" = "healthy" ]; then
            ok "AXiomEngine Router is already active and healthy on port $ROUTER_PORT."
        else
            warn "AXiomEngine Router detected on port $ROUTER_PORT but is unhealthy."
            kill_process "$PID_TO_MANAGE"
            if is_port_in_use $ROUTER_PORT; then
                warn "Port $ROUTER_PORT is still in use after kill attempt. Selecting fallback port..."
                ROUTER_PORT=$(find_available_port $((ROUTER_PORT + 1)))
            fi
            start_router "$ROUTER_PORT"
        fi
    else
        warn "Port $ROUTER_PORT is in use by another application (PIDs: $PIDS_ROUTER)."
        ROUTER_PORT=$(find_available_port $((ROUTER_PORT + 1)))
        info "Selected alternative port $ROUTER_PORT for Router."
        start_router "$ROUTER_PORT"
    fi
else
    start_router "$ROUTER_PORT"
fi

# 5. C2 Dashboard Server
hdr "5. Launching C2 Dashboard Server"
DASHBOARD_PORT=8765

start_dashboard() {
    local port="$1"
    info "Starting Dashboard on port $port..."
    export PYTHONPATH="${PYTHONPATH:-}:."
    nohup "$VENV/bin/python" scripts/governance_dashboard_server.py --port "$port" > logs/dashboard.log 2>&1 &
    info "Waiting for Dashboard to initialize..."
    sleep 3
    local check
    check=$(check_dashboard_health "$port")
    if [ "$check" = "healthy" ]; then
        ok "C2 Dashboard successfully active on port $port."
    else
        warn "Dashboard started but port $port is not responding healthy yet. Check logs/dashboard.log"
    fi
}

if is_port_in_use $DASHBOARD_PORT; then
    PIDS_DASHBOARD=$(get_pid_on_port $DASHBOARD_PORT)
    IS_OUR_APP=0
    PID_TO_MANAGE=""
    for pid in $PIDS_DASHBOARD; do
        if [ "$(get_process_app_type "$pid")" = "dashboard" ]; then
            IS_OUR_APP=1
            PID_TO_MANAGE="$pid"
            break
        fi
    done

    if [ $IS_OUR_APP -eq 1 ]; then
        HEALTH=$(check_dashboard_health $DASHBOARD_PORT)
        if [ "$HEALTH" = "healthy" ]; then
            ok "C2 Dashboard is already active and healthy on port $DASHBOARD_PORT."
        else
            warn "C2 Dashboard detected on port $DASHBOARD_PORT but is unhealthy."
            kill_process "$PID_TO_MANAGE"
            if is_port_in_use $DASHBOARD_PORT; then
                warn "Port $DASHBOARD_PORT is still in use after kill attempt. Selecting fallback port..."
                DASHBOARD_PORT=$(find_available_port $((DASHBOARD_PORT + 1)))
            fi
            start_dashboard "$DASHBOARD_PORT"
        fi
    else
        warn "Port $DASHBOARD_PORT is in use by another application (PIDs: $PIDS_DASHBOARD)."
        DASHBOARD_PORT=$(find_available_port $((DASHBOARD_PORT + 1)))
        info "Selected alternative port $DASHBOARD_PORT for Dashboard."
        start_dashboard "$DASHBOARD_PORT"
    fi
else
    start_dashboard "$DASHBOARD_PORT"
fi

# 6. Preload Ollama Models into VRAM
hdr "6. Preloading Ollama Models"

preload_model() {
    local port="$1"
    local model="$2"
    local label="$3"
    
    info "Preloading $model on port $port ($label)..."
    # Send a minimal generate request with keep_alive to load model into VRAM
    local resp
    resp=$(curl -sf --max-time 90 "http://127.0.0.1:${port}/api/generate" \
        -d "{\"model\": \"${model}\", \"prompt\": \"hi\", \"stream\": false, \"options\": {\"num_predict\": 1}}" 2>&1) || true
    
    if echo "$resp" | grep -q '"response"'; then
        ok "$model loaded into VRAM on port $port ($label)"
    else
        warn "$model preload on port $port may have failed (model might still be loading)"
    fi
}

# Preload the default PI model (qwen3.6:27b on P40 lane)
if curl -sf --max-time 1 "http://127.0.0.1:11437/api/tags" &>/dev/null; then
    preload_model 11437 "qwen3.6:27b" "P40 — PI default"
fi

# Preload the researcher model (gemma4:e2b on RTX 3070 lane)  
if curl -sf --max-time 1 "http://127.0.0.1:11436/api/tags" &>/dev/null; then
    preload_model 11436 "gemma4:e2b" "RTX 3070 — Researcher"
fi

# 7. PI Hosted Agent (Node.js coding-agent in RPC mode)
hdr "7. Launching PI Hosted Agent"
PI_CLI_PATH="$PROJECT_ROOT/pi/pi-mono-main/packages/coding-agent/dist/cli.js"
PI_PID_FILE="$PROJECT_ROOT/logs/pi_hosted.pid"
PI_MONO_DIR="$PROJECT_ROOT/pi/pi-mono-main"

# Guard: the coding-agent imports its sibling workspace packages by their
# published names (@mariozechner/pi-ai, /pi-agent-core, /pi-tui). Those resolve
# through npm-workspace symlinks under node_modules/@mariozechner/. If the
# symlinks are missing (fresh checkout, moved tree, partial install), the agent
# dies at startup with ERR_MODULE_NOT_FOUND and every PI mode silently fails.
# Recreate them automatically so this can never break quietly again.
ensure_pi_workspace_links() {
    local link_dir="$PI_MONO_DIR/node_modules/@mariozechner"
    local need_install=0
    for pkg in pi-ai pi-agent-core pi-tui pi-coding-agent; do
        if [ ! -e "$link_dir/$pkg" ]; then
            need_install=1
            break
        fi
    done

    if [ "$need_install" -eq 0 ]; then
        ok "PI workspace package links present."
        return 0
    fi

    if [ ! -d "$PI_MONO_DIR" ]; then
        warn "PI monorepo not found at $PI_MONO_DIR; cannot link workspace packages."
        return 1
    fi

    warn "PI workspace package links missing. Running 'npm install' to recreate them..."
    if ! command -v npm >/dev/null 2>&1; then
        fail "npm not found in PATH. Install Node.js/npm, then re-run."
        return 1
    fi

    # --offline first (packages are usually already cached/vendored); fall back
    # to a normal install if that fails.
    if (cd "$PI_MONO_DIR" && npm install --offline >/dev/null 2>&1) \
       || (cd "$PI_MONO_DIR" && npm install >/dev/null 2>&1); then
        # Verify the critical link actually exists now.
        if [ -e "$link_dir/pi-ai" ]; then
            ok "PI workspace package links created."
            return 0
        fi
    fi
    fail "Failed to create PI workspace links. Run manually: cd pi/pi-mono-main && npm install"
    return 1
}

start_pi_hosted() {
    if [ ! -f "$PI_CLI_PATH" ]; then
        warn "PI coding-agent not built. Skipping hosted PI."
        warn "  Expected: $PI_CLI_PATH"
        warn "  Run: cd pi/pi-mono-main && npm install && npm run build"
        return
    fi

    # Make sure workspace package links exist before launching, otherwise the
    # agent will crash with ERR_MODULE_NOT_FOUND.
    ensure_pi_workspace_links || {
        warn "Skipping hosted PI: workspace links could not be ensured."
        return
    }

    export PI_CODING_AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
    export PI_HOSTED=1
    export AXIOMENGINE_ROOT="$PROJECT_ROOT"

    mkdir -p "$PI_CODING_AGENT_DIR"

    info "Starting PI coding-agent (Node.js) in RPC mode..."
    nohup node "$PI_CLI_PATH" --mode rpc > "$PROJECT_ROOT/logs/pi_hosted.log" 2>&1 &
    local pi_pid=$!
    echo "$pi_pid" > "$PI_PID_FILE"
    sleep 2

    if kill -0 "$pi_pid" 2>/dev/null; then
        ok "PI hosted agent running (PID=$pi_pid, backend=node)"
    else
        warn "PI hosted agent failed to start. Check logs/pi_hosted.log"
    fi
}

# Check if PI is already running
if [ -f "$PI_PID_FILE" ]; then
    OLD_PID=$(cat "$PI_PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        ok "PI hosted agent already running (PID=$OLD_PID)"
    else
        info "Stale PI PID file found. Restarting..."
        rm -f "$PI_PID_FILE"
        start_pi_hosted
    fi
else
    start_pi_hosted
fi

hdr "Final Port Allocation & Active Services"
info "AXiomEngine Router:    http://127.0.0.1:${ROUTER_PORT}"
info "C2 Dashboard Server:   http://127.0.0.1:${DASHBOARD_PORT}"
if [ -f "$PI_PID_FILE" ] && kill -0 "$(cat "$PI_PID_FILE")" 2>/dev/null; then
    info "PI Hosted Agent:       PID=$(cat "$PI_PID_FILE") (RPC via stdin/stdout)"
fi
ok "Startup sequence complete!"

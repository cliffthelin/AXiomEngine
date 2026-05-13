#!/usr/bin/env bash
# AXiomEngine Quick Status Dashboard
# Run anytime: bash scripts/status.sh

RESET='\033[0m'; BOLD='\033[1m'; GREEN='\033[0;32m'
YELLOW='\033[0;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'

ok()   { echo -e "  ${GREEN}✅ $*${RESET}"; }
warn() { echo -e "  ${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "  ${RED}❌ $*${RESET}"; }
hdr()  { echo -e "\n${BOLD}${CYAN}── $* ─────────────────────────────────────${RESET}"; }

echo -e "${BOLD}AXiomEngine Status — $(date)${RESET}"

hdr "GPU Health"
nvidia-smi --query-gpu=index,name,temperature.gpu,power.draw,memory.used,memory.total \
    --format=csv,noheader 2>/dev/null | while IFS=',' read idx name temp power used total; do
    temp=$(echo $temp | tr -d ' ')
    [ "$temp" -gt 85 ] && \
        fail "GPU$idx:$name ${temp}°C CRITICAL" || \
        ok "GPU$idx:$name ${temp}°C | $power | ${used}/${total}"
done || fail "nvidia-smi not available"

hdr "Compute Processes"
nvidia-smi --query-compute-apps=gpu_uuid,pid,name,used_memory \
    --format=csv,noheader 2>/dev/null | head -6 | while IFS=',' read uuid pid name mem; do
    ok "PID $pid: $(basename ${name// /}) — $mem"
done

hdr "Services"
for svc in "Port 8080 (snap/llama):http://127.0.0.1:8080/health" \
           "Port 8330 (nemotron):http://127.0.0.1:8330/health" \
           "Port 9001 (Router):http://127.0.0.1:9001/health" \
           "Port 11434 (Ollama):http://127.0.0.1:11434/api/version"; do
    label="${svc%%:*}"
    url="${svc#*:}"
    if curl -sf --max-time 2 "$url" &>/dev/null; then
        ok "$label"
    else
        warn "$label — DOWN"
    fi
done

# Valkey
if command -v valkey-cli &>/dev/null && valkey-cli ping &>/dev/null 2>&1; then
    ok "Valkey (port 6379)"
elif command -v redis-cli &>/dev/null && redis-cli ping &>/dev/null 2>&1; then
    ok "Valkey-compatible (port 6379)"
else
    warn "Valkey — not running"
fi

# Postgres
pg_isready -p 5433 -q 2>/dev/null && ok "Postgres 18 (port 5433)" || warn "Postgres 18 — not ready"
pg_isready -p 5432 -q 2>/dev/null && ok "Postgres 16 (port 5432)"

hdr "Ollama Models"
ollama list 2>/dev/null | tail -n +2 | while read line; do
    ok "$line"
done

hdr "Active Mode"
MODE=$(curl -sf http://127.0.0.1:9001/health 2>/dev/null | python3 -c \
    "import sys,json; d=json.load(sys.stdin); print('Router UP')" 2>/dev/null || echo "Router DOWN")
echo "  $MODE"
ROUTER_MODE=$(command -v valkey-cli &>/dev/null && valkey-cli get "router:active_mode" 2>/dev/null || \
              command -v redis-cli &>/dev/null && redis-cli get "router:active_mode" 2>/dev/null || echo "1 (split)")
ok "Mode: $ROUTER_MODE"

echo ""

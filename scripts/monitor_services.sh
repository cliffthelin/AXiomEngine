#!/usr/bin/env bash
# =============================================================================
# AXiomEngine Service Monitor and Backup Automation
# =============================================================================
# This script monitors core agent service ports, checks GPU status,
# and performs a timestamped workspace backup.
#
# Recommended scheduling via User Crontab:
#   Run "crontab -e" and add the following line to automate hourly:
#   0 * * * * /mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/agentos/scripts/monitor_services.sh >> /mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/agentos/logs/cron_monitor.log 2>&1
# =============================================================================

set -u

PROJECT_DIR="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/agentos"
BACKUP_DIR="$HOME/axiom_backups"
LOG_FILE="$PROJECT_DIR/logs/monitor_services.log"

# Create directories if they do not exist
mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_msg "=================== SERVICE RUN START ==================="

# 1. Check Service Ports
declare -A SERVICES=(
    ["9001"]="AXiomEngine Router"
    ["8766"]="C2 Dashboard Server"
    ["8330"]="Archon Swarm Console"
    ["6379"]="Valkey/Redis Cache"
    ["11434"]="Ollama/LLM Proxy"
)

log_msg "--- Checking Port Health ---"
for port in "${!SERVICES[@]}"; do
    if lsof -i :"$port" &>/dev/null || curl -sf "http://127.0.0.1:$port/" &>/dev/null; then
        log_msg "✅ Port $port (${SERVICES[$port]}): ACTIVE"
    else
        log_msg "⚠️  Port $port (${SERVICES[$port]}): INACTIVE"
    fi
done

# 2. Check GPU Health
log_msg "--- Checking GPU Health ---"
if command -v nvidia-smi &>/dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu --format=csv,noheader,nounits 2>/dev/null)
    if [ $? -eq 0 ] && [ -n "$GPU_INFO" ]; then
        log_msg "✅ GPU status: OK - $GPU_INFO"
    else
        log_msg "❌ GPU status: FAILED (nvidia-smi query returned error)"
    fi
else
    log_msg "ℹ️  GPU status: Not Applicable (nvidia-smi not found in path)"
fi

# 3. Perform Timestamped Backup
log_msg "--- Initiating Workspace Backup ---"
BACKUP_FILE="$BACKUP_DIR/axiom_backup_$(date +%F_%H-%M).tar.gz"

# Maintain last 10 backups to prevent disk bloat
tar --exclude='.git' \
    --exclude='node_modules' \
    --exclude='cache' \
    -czf "$BACKUP_FILE" -C "$PROJECT_DIR" . &>/dev/null

if [ $? -eq 0 ]; then
    log_msg "✅ Backup successfully created: $BACKUP_FILE"
    
    # Prune old backups, keeping only the 10 most recent
    cd "$BACKUP_DIR" && ls -t axiom_backup_*.tar.gz 2>/dev/null | tail -n +11 | xargs -r rm --
    log_msg "🧹 Backup cleanup complete (retaining 10 most recent backups)"
else
    log_msg "❌ Backup failed to create."
fi

log_msg "==================== SERVICE RUN END ===================="

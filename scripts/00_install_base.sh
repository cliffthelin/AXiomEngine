#!/usr/bin/env bash
# =============================================================================
# AXiomEngine Phase 0 — System Dependencies (UPDATED: Postgres 18)
# Run in a terminal with sudo:  sudo bash 00_install_base.sh
# =============================================================================
set -euo pipefail

AXIOMENGINE="/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine"
PG_PORT=5433     # Postgres 18 default on this system
PG_DSN="postgresql://axiomengine:axiomengine_local_dev@localhost:${PG_PORT}/axiomengine"

echo "============================================"
echo " AXiomEngine Base Install — Ubuntu 26.04"
echo " Postgres 18 (port $PG_PORT)"
echo "============================================"

# ── 1. pgvector for Postgres 18 ──────────────────────────────────────────────
echo "[1/7] Installing postgresql-18-pgvector..."
apt-get install -y postgresql-18-pgvector
echo "  ✅ pgvector installed"

# ── 2. Valkey ────────────────────────────────────────────────────────────────
echo "[2/7] Installing Valkey..."
if ! command -v valkey-server &>/dev/null; then
    apt-get install -y valkey valkey-tools 2>/dev/null && echo "  ✅ Valkey from apt" || {
        echo "  Not in apt — building from source..."
        VALKEY_VER="8.1.1"
        curl -fsSL "https://github.com/valkey-io/valkey/archive/refs/tags/${VALKEY_VER}.tar.gz" \
            -o /tmp/valkey.tar.gz
        tar -xf /tmp/valkey.tar.gz -C /tmp
        cd "/tmp/valkey-${VALKEY_VER}"
        make -j$(nproc)
        make install
        cd -
        echo "  ✅ Valkey built from source"
    }
else
    echo "  ✅ Valkey already installed: $(valkey-server --version | head -1)"
fi

# ── 3. Valkey systemd service ─────────────────────────────────────────────────
echo "[3/7] Configuring Valkey service..."
# The package creates the user and a default config. We will update the config.
mkdir -p /etc/valkey /var/lib/valkey /var/log/valkey
chown valkey:valkey /var/lib/valkey /var/log/valkey

# Update the native config file
cat > /etc/valkey/valkey.conf << 'VCONF'
bind 127.0.0.1
port 6379
daemonize no
loglevel notice
logfile /var/log/valkey/valkey.log
dir /var/lib/valkey
maxmemory 8gb
maxmemory-policy allkeys-lru
save ""
VCONF

# Use the package's native service name
systemctl daemon-reload
systemctl enable --now valkey-server
echo "  Valkey: $(systemctl is-active valkey-server)"

# ── 4. Postgres 18 — axiomengine database ────────────────────────────────────────
echo "[4/7] Setting up AXiomEngine database in Postgres 18 (port $PG_PORT)..."

# Create role if missing
sudo -u postgres psql -p "$PG_PORT" << 'PGROLE'
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'axiomengine') THEN
        CREATE USER axiomengine WITH PASSWORD 'axiomengine_local_dev' CREATEDB;
        RAISE NOTICE 'Created axiomengine role';
    ELSE
        ALTER USER axiomengine WITH PASSWORD 'axiomengine_local_dev';
        RAISE NOTICE 'Updated axiomengine role password';
    END IF;
END$$;
PGROLE

# Create DB if missing
sudo -u postgres psql -p "$PG_PORT" -tc \
    "SELECT 1 FROM pg_database WHERE datname='axiomengine'" | grep -q 1 || \
    sudo -u postgres createdb -p "$PG_PORT" -O axiomengine axiomengine
echo "  ✅ Database axiomengine ready"

# Create schema
sudo -u postgres psql -p "$PG_PORT" -d axiomengine << 'PGSCHEMA'
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- PDD Rules (authoritative context store)
CREATE TABLE IF NOT EXISTS pdd_rules (
    rule_id     TEXT PRIMARY KEY,
    scope       TEXT NOT NULL DEFAULT 'core',
    title       TEXT,
    content     TEXT NOT NULL,
    embedding   vector(768),
    version     INT DEFAULT 1,
    active      BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS pdd_rules_embedding_idx
    ON pdd_rules USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS pdd_rules_scope_idx ON pdd_rules(scope);

-- PDD Rule Mutation Proposals (R-PDD-SWARM-001, Phase 6/7)
CREATE TABLE IF NOT EXISTS pdd_proposals (
    proposal_id  BIGSERIAL PRIMARY KEY,
    rule_id      TEXT,
    agent_name   TEXT,
    change_type  TEXT NOT NULL, -- new | update | delete
    title        TEXT,
    content      TEXT NOT NULL,
    rationale    TEXT,
    status       TEXT NOT NULL DEFAULT 'pending', -- pending | approved | rejected
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    updated_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS pdd_proposals_status_idx ON pdd_proposals(status);

-- Agent Audit Trail (R-PDD-AUDIT-001)
CREATE TABLE IF NOT EXISTS agent_audit (
    id           BIGSERIAL PRIMARY KEY,
    session_id   TEXT,
    agent_name   TEXT,
    model        TEXT,
    model_ver    TEXT,
    rules_cited  TEXT[],
    prompt_hash  TEXT,
    output_hash  TEXT,
    backend      TEXT,
    tokens_in    INT,
    tokens_out   INT,
    latency_ms   INT,
    drift_flag   BOOLEAN DEFAULT FALSE,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS agent_audit_session_idx ON agent_audit(session_id);
CREATE INDEX IF NOT EXISTS agent_audit_time_idx ON agent_audit(created_at DESC);

-- Agent Sessions
CREATE TABLE IF NOT EXISTS agent_sessions (
    session_id   TEXT PRIMARY KEY,
    agent_name   TEXT,
    mode         TEXT DEFAULT 'split_llm',
    context      JSONB DEFAULT '{}',
    created_at   TIMESTAMPTZ DEFAULT NOW(),
    last_active  TIMESTAMPTZ DEFAULT NOW()
);

-- Model Registry
CREATE TABLE IF NOT EXISTS model_registry (
    model_id     TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    backend      TEXT NOT NULL,
    endpoint     TEXT,
    vram_mb      INT,
    primary_gpu  INT,
    tags         TEXT[] DEFAULT '{}',
    active       BOOLEAN DEFAULT TRUE,
    registered   TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO model_registry VALUES
    ('nemotron-30b-snap', 'Nemotron-3-Nano-30B', 'snap',
     'http://127.0.0.1:8080', 25646, 1, ARRAY['split','llm'], true, NOW()),
    ('qwen3.6-ollama',    'Qwen 3.6 35B',        'ollama',
     'http://127.0.0.1:11434', 23000, 0, ARRAY['split','llm','qwen'], true, NOW())
ON CONFLICT (model_id) DO NOTHING;

SELECT 'Schema OK: ' || count(*) || ' tables' 
FROM information_schema.tables 
WHERE table_schema='public';

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO axiomengine;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO axiomengine;
PGSCHEMA

echo "  ✅ Schema created"

# ── 5. Enable Postgres 18 Async I/O ──────────────────────────────────────────
echo "[5/7] Tuning Postgres 18 for AI workloads..."
sudo -u postgres psql -p "$PG_PORT" << 'PGTUNE'
ALTER SYSTEM SET io_method = 'io_uring';
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '32GB';
ALTER SYSTEM SET maintenance_work_mem = '1GB';
ALTER SYSTEM SET max_connections = '200';
SELECT pg_reload_conf();
PGTUNE
echo "  ✅ Postgres 18 tuned (io_uring AIO enabled)"

# ── 6. NVIDIA persistence mode ────────────────────────────────────────────────
echo "[6/7] Enabling NVIDIA persistence mode..."
nvidia-smi -pm 1 && echo "  ✅ Persistence mode ON" || echo "  ⚠️  Could not set persistence"
nvidia-smi --auto-boost-default=0 || true

# ── 7. GPU Thermal Monitor ────────────────────────────────────────────────────
echo "[7/7] Installing P40 thermal monitor..."
cat > /etc/systemd/system/gpu-thermal-monitor.service << 'TSVC'
[Unit]
Description=GPU Thermal Monitor (P40 passive cooling safety)
After=multi-user.target

[Service]
Type=simple
ExecStart=/bin/bash -c '\
    while true; do \
        nvidia-smi --query-gpu=index,name,temperature.gpu --format=csv,noheader 2>/dev/null | \
        while IFS=, read idx name temp; do \
            temp=$(echo $temp | tr -d " "); \
            if [ "${temp:-0}" -gt 85 ]; then \
                echo "CRITICAL GPU${idx} ${name} ${temp}C" | systemd-cat -t gpu-thermal -p crit; \
                wall "⚠ AXiomEngine WARNING: ${name} (GPU${idx}) is ${temp}°C — stop inference!"; \
            fi; \
        done; \
        sleep 30; \
    done'
Restart=always

[Install]
WantedBy=multi-user.target
TSVC

systemctl daemon-reload
systemctl enable --now gpu-thermal-monitor
echo "  ✅ Thermal monitor active"

echo ""
echo "============================================"
echo " ✅ Phase 0 Complete!"
echo ""
echo " Next steps:"
echo "   cd $AXIOMENGINE"
echo "   # Load PDD rules into Postgres:"
echo "   ~/.axiomengine_venv/bin/python pdd/load_rules.py"
echo "   # Start the router:"
echo "   bash scripts/01_start_router.sh"
echo "============================================"

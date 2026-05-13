# Hardware & Resource Constraints Extraction

Based on the provided source code, here are the documented hardware limits, power/thermal thresholds, and resource management rules. This output is structured for direct inclusion in your system design documentation.

## 1. Target Hardware & Role Assignment
| Component | Identifier | Role in Stack |
|-----------|------------|---------------|
| **NVIDIA Tesla P40** | `GPU_ID = 1` | Primary compute target. Subject to dynamic power/thermal governance. |
| **NVIDIA RTX 3070** | `GPU_ID = 0` | Secondary GPU. Monitored for VRAM availability during mission execution. |
| **Host System** | N/A | Orchestrates task shards, monitors RAM, and enforces failover/recovery. |

## 2. P40 Power Constraints
The `gpu_thermal_optimizer.py` script enforces stepped power limits via `nvidia-smi -pl`. Limits are applied dynamically every `2 seconds`.

| State | Power Limit | Trigger Condition |
|-------|-------------|-------------------|
| **Normal / Max** | `220W` | Base limit; restored when temp ≤ `70°C` |
| **Warning** | `180W` | Activated when temp ≥ `75°C` |
| **Critical** | `150W` | Activated when temp ≥ `82°C` |

⚠️ **Execution Requirement:** Power limit changes require root privileges. Failure to apply limits exits the optimizer with `sys.exit(1)`.

## 3. P40 Thermal Limits & Hysteresis Logic
Temperature thresholds use strict hysteresis to prevent power-state oscillation during rapid thermal fluctuations:

| Threshold | Value | Action |
|-----------|-------|--------|
| `TEMP_WARNING` | `75°C` | Steps power down to `180W` |
| `TEMP_CRITICAL` | `82°C` | Steps power down to `150W` |
| `TEMP_RECOVERY` | `70°C` | Restores power to `220W` |

**Behavioral Note:** The optimizer only steps power limits when the current temperature crosses a threshold *and* the current power limit differs from the target. Once at `180W`, it will not drop further until `82°C` is hit. Recovery requires cooling to `≤70°C`, creating a `5°C–12°C` thermal buffer zone.

## 4. VRAM & System Memory Constraints
| Resource | Buffer Limit | Monitoring Target | Enforcement Status |
|----------|--------------|-------------------|---------------------|
| **System RAM** | `8 GB` free | Host system (`psutil`) | Warning logged; throttling stub reserved |
| **VRAM** | `500 MB` free | `GPU_ID = 0` (RTX 3070) | Warning logged; throttling stub reserved |

🔍 **Architectural Note:** The code explicitly monitors VRAM on the **RTX 3070**, not the P40. No hardcoded VRAM limit exists for the P40 in this context. The P40's native `24GB GDDR5` is implicitly available for compute tasks, while the watchdog ensures the RTX 3070 (likely handling inference/UI/lightweight tasks) retains a `500MB` safety margin.

## 5. Resource Orchestration & Failover Rules
- **Stall Detection:** `900s` (15 mins) of zero progress (`rules_completed` not incrementing) triggers automatic kill of stalled processes (`DataCatalogFactory.py`, `ollama`) and service restart.
- **Polling Cadence:** 
  - Thermal/Power: `2s`
  - Memory/VRAM & Progress: `60s`
- **Grace Degradation:** Thermal protection operates independently of task queues. Power limits drop automatically before OS-level thermal throttling or emergency shutdowns can occur.

## 6. Open Constraints / Recommendations
1. **P40 VRAM Monitoring Gap:** Consider adding a `VRAM_BUFFER` check for `GPU_ID = 1` if the P40 runs memory-intensive models.
2. **VRAM Throttling Stub:** The `watchdog` logs warnings but lacks active throttling logic. Implement task pausing or process suspension when `VRAM_BUFFER` or `RAM_BUFFER` is breached.
3. **Power Limit Validation:** Add fallback handling if `nvidia-smi -pl` fails intermittently (currently exits entirely; could loop with exponential backoff).

---
*Extraction complete. Ready for integration into `_reversa_sdd/resource.md` or `hardware_constraints.md`.*
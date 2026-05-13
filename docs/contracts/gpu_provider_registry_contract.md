# AXiomEngine GPU Provider Registry Contract (v0.1.0)

## Objective
Provide a unified, read-only inventory of available GPU compute resources and local inference providers (Ollama, llama-server).

## Detection Requirements

### 1. Hardware (NVIDIA)
- **Source**: `nvidia-smi`
- **Fields**: 
  - Index, Name, UUID
  - Memory (Total, Used, Free)
  - Utilization (GPU, Memory)
  - Power (Draw, Limit)
  - Temperature
  - Persistence Mode
  - Display Active Status

### 2. Provider: Ollama
- **Source**: `ollama ps`, `ollama list`, and API probe (`/api/tags`)
- **Fields**:
  - Running models (Name, Size, Processor, Context, Expiry)
  - Installed models (Name, Size, Details)

### 3. Provider: llama-server
- **Source**: `ps aux` discovery and API probe (`/health`, `/v1/models`)
- **Fields**:
  - Process ID (PID)
  - Bound Port and Host
  - Loaded Model Alias/Path
  - Health Status

## Operational Constraints
- **Read-Only**: Must not modify any system state (power limits, persistence mode, etc.).
- **Non-Destructive**: Must not kill or restart any processes.
- **Resilient**: Must run on systems without NVIDIA hardware (returning empty/null fields).
- **Silent**: Must not produce side-effects or heavy logs unless requested.

## Output Format
- **Format**: JSON (stdout)
- **Optional File**: `docs/audit/gpu_provider_report.json`

## Audit Defense
The generated report must serve as a "Point-in-Time" forensic record of the machine's inference capability, suitable for inclusion in governance audit trails.

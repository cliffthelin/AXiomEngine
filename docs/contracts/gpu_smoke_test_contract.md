# GPU Smoke Test Contract (v1.0.0)

## Objective
Provide a forensic record of GPU resource availability and inference readiness within the AXiomEngine governance stack.

## Data Schema
The output file `docs/audit/gpu_smoke_report.json` must adhere to the following structure:

```json
{
  "timestamp": "ISO-8601",
  "detected_gpu_count": "integer",
  "driver_version": "string",
  "cuda_version": "string",
  "gpus": [
    {
      "index": "integer",
      "name": "string",
      "memory_total_mb": "integer",
      "memory_used_mb": "integer",
      "utilization_gpu_percent": "integer",
      "temperature_c": "integer"
    }
  ],
  "active_processes": [
    {
      "gpu_index": "integer",
      "pid": "integer",
      "process_name": "string",
      "used_memory_mb": "integer"
    }
  ],
  "ollama": {
    "detected": "boolean",
    "models": ["string"],
    "status": "string"
  },
  "report_status": "STABLE | WARNING | NO_GPU_DETECTED"
}
```

## Constraints
1. **Non-Invasive**: The script must not modify system state or GPU configurations.
2. **Subprocess Only**: Use `nvidia-smi` as the primary source of truth. Do not require PyCUDA or specialized drivers for detection.
3. **Audit Readiness**: All output must be written to the `docs/audit/` directory with a consistent naming convention.

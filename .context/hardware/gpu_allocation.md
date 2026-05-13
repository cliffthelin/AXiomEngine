# Hardware Allocation — Authoritative Definition
# R-PDD-GOV-001: Single source of truth for GPU assignment per mode.

## GPU Inventory
| Device | PCI | nvidia-smi Index | VRAM | Architecture | Cooling |
|---|---|---|---|---|---|
| RTX 3070 | 01:00.0 | GPU 0 | 8 GB | Ampere (sm_86) | Active fan |
| Tesla P40 | 05:00.0 | GPU 1 | 24 GB | Pascal (sm_60) | **PASSIVE — needs airflow** |
| AMD Raphael | 0d:00.0 | — | Shared | RDNA 2 | Integrated |

## Mode Assignment Table
| Mode | RTX 3070 (GPU 0) | Tesla P40 (GPU 1) | AMD Raphael | Display |
|---|---|---|---|---|
| **1: Split LLM** | LLM head + KV | LLM body | **Display** | Raphael |
| **2: ComfyUI** | VAE/CLIP/ControlNet | UNet/Diffusion | **Display** | Raphael |
| **3: Direct** | Dedicated model OR idle | Dedicated model OR idle | **Display** | Raphael |
| **4: Gaming** | **Primary render + display** | Shader cache (compute) | Idle | RTX 3070 |

## P40 Thermal Limits (CRITICAL)
The Tesla P40 is a **passive-cooled datacenter card** in a consumer chassis.

| State | Temp | Action |
|---|---|---|
| Normal | < 75°C | None |
| Warning | 75-85°C | Reduce context size, check airflow |
| **CRITICAL** | > 85°C | **Stop inference immediately** |
| Shutdown | > 90°C | Automatic GPU throttle |

Monitor: `watch -n5 nvidia-smi --query-gpu=index,name,temperature.gpu,power.draw --format=csv`

## CUDA Architecture Note
Mixed Pascal + Ampere requires both targets at compile time:
```
-DCMAKE_CUDA_ARCHITECTURES="60;86"
```
Without this, llama.cpp compiled only for Ampere will FAIL on P40.

## Display Lock Requirements (Modes 1-3)
AMD Raphael (iGPU) MUST be the display adapter in Modes 1-3.
Wayland compositor should use amdgpu driver.
Status check: `glxinfo | grep renderer` — must show Radeon Raphael.

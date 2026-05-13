import pytest
from unittest.mock import patch, MagicMock
import json
import os
import scripts.gpu_smoke_test as gpu_smoke_test

MOCK_SMI_OUTPUT = """0, NVIDIA GeForce RTX 3070, 8192, 2105, 4, 42
1, Tesla P40, 23040, 171, 0, 46"""

MOCK_VERSION_OUTPUT = "580.142"

MOCK_FULL_SMI = """
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.142                Driver Version: 580.142        CUDA Version: 13.0     |
+-----------------------------------------------------------------------------------------+
"""

MOCK_OLLAMA_LIST = """NAME            ID              SIZE      MODIFIED
qwen3.6:27b     1234567890ab    16 GB     2 hours ago
gemma:7b        abcdef123456    5.0 GB    1 day ago
"""

@patch("scripts.gpu_smoke_test.run_command")
def test_get_gpu_data(mock_run):
    def side_effect(cmd):
        if "--query-gpu=index" in cmd[1]:
            return MOCK_SMI_OUTPUT
        if "--query-gpu=driver_version" in cmd[1]:
            return MOCK_VERSION_OUTPUT
        if cmd == ["nvidia-smi"]:
            return MOCK_FULL_SMI
        return None
    
    mock_run.side_effect = side_effect
    
    driver, cuda, gpus = gpu_smoke_test.get_gpu_data()
    
    assert driver == "580.142"
    assert cuda == "13.0"
    assert len(gpus) == 2
    assert gpus[0]["name"] == "NVIDIA GeForce RTX 3070"
    assert gpus[1]["memory_total_mb"] == 23040

@patch("scripts.gpu_smoke_test.run_command")
def test_get_ollama_status(mock_run):
    mock_run.return_value = MOCK_OLLAMA_LIST
    
    status = gpu_smoke_test.get_ollama_status()
    
    assert status["detected"] is True
    assert "qwen3.6:27b" in status["models"]
    assert "gemma:7b" in status["models"]

@patch("scripts.gpu_smoke_test.run_command")
@patch("scripts.gpu_smoke_test.get_gpu_data")
@patch("scripts.gpu_smoke_test.get_active_processes")
@patch("scripts.gpu_smoke_test.get_ollama_status")
def test_main_logic(mock_ollama, mock_proc, mock_gpu, mock_run, tmp_path):
    mock_gpu.return_value = ("580.142", "13.0", [{"index": 0, "name": "GPU", "memory_total_mb": 8000, "memory_used_mb": 100, "utilization_gpu_percent": 0, "temperature_c": 40}])
    mock_proc.return_value = []
    mock_ollama.return_value = {"detected": True, "models": ["qwen3.6:27b"], "status": "READY"}
    
    report_file = tmp_path / "gpu_smoke_report.json"
    with patch("scripts.gpu_smoke_test.REPORT_PATH", str(report_file)):
        gpu_smoke_test.main()
        
    assert os.path.exists(report_file)
    with open(report_file) as f:
        data = json.load(f)
        assert data["detected_gpu_count"] == 1
        assert data["ollama"]["models"][0] == "qwen3.6:27b"

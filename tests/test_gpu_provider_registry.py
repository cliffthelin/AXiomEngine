import unittest
from unittest.mock import patch, MagicMock
import json
import sys
from pathlib import Path

# Add scripts dir to path
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from gpu_provider_registry import GPUProviderRegistry

class TestGPUProviderRegistry(unittest.TestCase):

    @patch("gpu_provider_registry.subprocess.run")
    def test_no_hardware(self, mock_run):
        """Test detection on a system with no NVIDIA GPUs."""
        # nvidia-smi returns error or empty
        mock_run.return_value = MagicMock(stdout="", stderr="command not found", check=False)
        
        registry = GPUProviderRegistry()
        report = registry.run_discovery()
        
        self.assertEqual(len(report["hardware"]["gpus"]), 0)
        self.assertFalse(report["providers"]["ollama"]["active"])
        self.assertFalse(report["providers"]["llama_server"]["active"])

    @patch("gpu_provider_registry.subprocess.run")
    def test_dual_gpu_with_providers(self, mock_run):
        """Test detection on a system with RTX 3070 and Tesla P40."""
        
        def side_effect(cmd, **kwargs):
            cmd_str = " ".join(cmd)
            if "nvidia-smi" in cmd_str:
                return MagicMock(stdout="0, RTX 3070, UUID-1, 8192, 1000, 7192, 5, 2, 50, 270, 45, Enabled, Enabled\n1, Tesla P40, UUID-2, 23040, 20000, 3040, 90, 40, 140, 180, 60, Enabled, Disabled")
            elif "which ollama" in cmd_str:
                return MagicMock(stdout="/usr/local/bin/ollama")
            elif "ollama list" in cmd_str:
                return MagicMock(stdout="NAME    ID    SIZE    MODIFIED\nqwen3.6:27b    a50e    17 GB    2 days ago")
            elif "ollama ps" in cmd_str:
                return MagicMock(stdout="NAME    ID    SIZE    PROCESSOR    CONTEXT    UNTIL\nqwen3.6:27b    a50e    25 GB    100% GPU    32768    4 minutes")
            elif "ps aux" in cmd_str:
                return MagicMock(stdout="root 5243 0.1 0.7 15490400 503748 ? Sl May11 1:49 llama-server --model /path/to/model.gguf --alias gemma-test --port 8336 --host 127.0.0.1")
            return MagicMock(stdout="")

        mock_run.side_effect = side_effect
        
        registry = GPUProviderRegistry()
        report = registry.run_discovery()
        
        # Hardware checks
        self.assertEqual(len(report["hardware"]["gpus"]), 2)
        self.assertEqual(report["hardware"]["gpus"][0]["name"], "RTX 3070")
        self.assertEqual(report["hardware"]["gpus"][1]["name"], "Tesla P40")
        self.assertEqual(report["hardware"]["gpus"][1]["utilization"]["gpu_pct"], 90)
        
        # Ollama checks
        self.assertTrue(report["providers"]["ollama"]["active"])
        self.assertEqual(len(report["providers"]["ollama"]["running"]), 1)
        self.assertEqual(report["providers"]["ollama"]["running"][0]["name"], "qwen3.6:27b")
        
        # llama-server checks
        self.assertTrue(report["providers"]["llama_server"]["active"])
        self.assertEqual(len(report["providers"]["llama_server"]["instances"]), 1)
        self.assertEqual(report["providers"]["llama_server"]["instances"][0]["port"], "8336")
        self.assertEqual(report["providers"]["llama_server"]["instances"][0]["alias"], "gemma-test")

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
OllamaController — Full programmatic control of Ollama models for AXiomEngine.

Provides both REST API and Python SDK interfaces for:
  - Model management (list, show, pull, push, delete, copy, create)
  - Lifecycle control (load, unload, switch models via keep_alive)
  - Inference (chat, generate, embed with streaming support)
  - Capabilities (tool calling, thinking, structured outputs, vision)
  - VRAM-aware operations (integrates with vgpu_manager)
  - Dual API support (native Ollama + OpenAI-compatible)

Reference: https://docs.ollama.com/api/introduction
"""

import json
import time
import logging
from typing import Any, Optional, Union, Generator, Callable
from pathlib import Path

import httpx

logger = logging.getLogger("axiomengine.ollama")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 120.0  # seconds for inference calls
MGMT_TIMEOUT = 30.0      # seconds for management calls (list, show, etc.)
PULL_TIMEOUT = 600.0      # seconds for model pull (large downloads)

# VRAM-based context length defaults (from docs)
VRAM_CONTEXT_MAP = [
    (24_000, 4096),    # < 24 GiB  → 4k
    (48_000, 32768),   # 24-48 GiB → 32k
    (float("inf"), 262144),  # ≥ 48 GiB → 256k
]


class OllamaError(Exception):
    """Base exception for Ollama API errors."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Ollama API error {status_code}: {message}")


class OllamaController:
    """
    Unified controller for all Ollama API operations.

    Usage:
        oc = OllamaController()
        models = oc.list_models()
        response = oc.chat("qwen3.6:27b", [{"role": "user", "content": "Hello"}])
        oc.switch_model("qwen3.6:27b", "deepseek-r1:14b")
    """

    def __init__(self, base_url: str = DEFAULT_BASE_URL, vgpu_manager=None):
        """
        Args:
            base_url: Ollama server URL (default: http://localhost:11434)
            vgpu_manager: Optional VGPUManager instance for VRAM-aware operations
        """
        self.base_url = base_url.rstrip("/")
        self.api_url = f"{self.base_url}/api"
        self.openai_url = f"{self.base_url}/v1"
        self.vgpu = vgpu_manager
        self._client = httpx.Client(timeout=DEFAULT_TIMEOUT)
        self._mgmt_client = httpx.Client(timeout=MGMT_TIMEOUT)

    def close(self):
        """Close HTTP clients."""
        self._client.close()
        self._mgmt_client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # -----------------------------------------------------------------------
    # Health & Version
    # -----------------------------------------------------------------------

    def is_alive(self) -> bool:
        """Check if the Ollama server is responding."""
        try:
            r = self._mgmt_client.get(self.base_url)
            return r.status_code == 200
        except httpx.ConnectError:
            return False

    def version(self) -> str:
        """Get the Ollama server version."""
        r = self._mgmt_client.get(f"{self.api_url}/version")
        self._check(r)
        return r.json().get("version", "unknown")

    # -----------------------------------------------------------------------
    # Model Discovery & Inspection
    # -----------------------------------------------------------------------

    def list_models(self) -> list[dict]:
        """
        List all locally installed models.

        Returns list of dicts with keys: name, model, modified_at, size,
        digest, details (format, family, parameter_size, quantization_level).
        """
        r = self._mgmt_client.get(f"{self.api_url}/tags")
        self._check(r)
        return r.json().get("models", [])

    def list_model_names(self) -> list[str]:
        """Return just the names of installed models."""
        return [m["name"] for m in self.list_models()]

    def list_running(self) -> list[dict]:
        """
        List models currently loaded in memory.

        Returns list of dicts with keys: name, model, size, digest, details,
        expires_at, size_vram, context_length.
        """
        r = self._mgmt_client.get(f"{self.api_url}/ps")
        self._check(r)
        return r.json().get("models", [])

    def list_running_names(self) -> list[str]:
        """Return just the names of running models."""
        return [m["name"] for m in self.list_running()]

    def show(self, model: str, verbose: bool = False) -> dict:
        """
        Show detailed model information.

        Returns: parameters, license, capabilities, modified_at, details,
                 template, model_info (architecture, context_length, etc.)
        """
        body = {"model": model}
        if verbose:
            body["verbose"] = True
        r = self._mgmt_client.post(f"{self.api_url}/show", json=body)
        self._check(r)
        return r.json()

    def get_capabilities(self, model: str) -> list[str]:
        """Get the list of supported capabilities for a model (e.g. completion, vision, tools)."""
        info = self.show(model)
        return info.get("capabilities", [])

    def get_context_length(self, model: str) -> Optional[int]:
        """Get the model's configured context length from model_info."""
        info = self.show(model)
        model_info = info.get("model_info", {})
        # Context length is stored under the model family key
        for key, val in model_info.items():
            if key.endswith(".context_length"):
                return val
        return None

    def model_exists(self, model: str) -> bool:
        """Check if a model is installed locally."""
        return model in self.list_model_names()

    def model_is_running(self, model: str) -> bool:
        """Check if a model is currently loaded in VRAM."""
        return model in self.list_running_names()

    # -----------------------------------------------------------------------
    # Model Management (pull, push, copy, delete, create)
    # -----------------------------------------------------------------------

    def pull(self, model: str, stream: bool = False) -> Union[dict, Generator]:
        """
        Pull (download) a model from the Ollama registry.

        If stream=True, yields progress dicts with status/completed/total.
        If stream=False, blocks until complete and returns final status.
        """
        body = {"model": model, "stream": stream}
        if stream:
            return self._stream_request("POST", f"{self.api_url}/pull", body, timeout=PULL_TIMEOUT)
        else:
            r = httpx.Client(timeout=PULL_TIMEOUT).post(f"{self.api_url}/pull", json=body)
            self._check(r)
            return r.json()

    def push(self, model: str, stream: bool = False) -> Union[dict, Generator]:
        """Push a model to the Ollama registry."""
        body = {"model": model, "stream": stream}
        if stream:
            return self._stream_request("POST", f"{self.api_url}/push", body, timeout=PULL_TIMEOUT)
        else:
            r = httpx.Client(timeout=PULL_TIMEOUT).post(f"{self.api_url}/push", json=body)
            self._check(r)
            return r.json()

    def copy(self, source: str, destination: str) -> bool:
        """Copy/alias a model. Returns True on success."""
        r = self._mgmt_client.post(
            f"{self.api_url}/copy",
            json={"source": source, "destination": destination}
        )
        return r.status_code == 200

    def delete(self, model: str) -> bool:
        """Delete a local model. Returns True on success."""
        r = self._mgmt_client.request(
            "DELETE", f"{self.api_url}/delete",
            json={"model": model}
        )
        return r.status_code == 200

    def create(
        self,
        model: str,
        from_model: Optional[str] = None,
        modelfile_content: Optional[str] = None,
        system: Optional[str] = None,
        parameters: Optional[dict] = None,
        stream: bool = False,
    ) -> Union[dict, Generator]:
        """
        Create a new model from a Modelfile or base model.

        Args:
            model: Name for the new model
            from_model: Base model to derive from (e.g. "qwen3.6:27b")
            modelfile_content: Raw Modelfile content string
            system: System prompt override
            parameters: Parameter overrides (temperature, num_ctx, etc.)
            stream: If True, yields progress dicts
        """
        body = {"model": model, "stream": stream}
        if from_model:
            body["from"] = from_model
        if modelfile_content:
            body["modelfile"] = modelfile_content
        if system:
            body["system"] = system
        if parameters:
            body["parameters"] = parameters

        if stream:
            return self._stream_request("POST", f"{self.api_url}/create", body)
        else:
            r = self._client.post(f"{self.api_url}/create", json=body)
            self._check(r)
            return r.json()

    # -----------------------------------------------------------------------
    # Model Lifecycle (load / unload / switch)
    # -----------------------------------------------------------------------

    def load_model(self, model: str, keep_alive: str = "5m") -> dict:
        """
        Pre-load a model into VRAM without generating text.

        Sends a minimal generate request to trigger loading.
        """
        if not self.model_exists(model):
            raise OllamaError(404, f"Model '{model}' is not installed. Pull it first.")

        body = {
            "model": model,
            "prompt": "",
            "keep_alive": keep_alive,
            "stream": False,
        }
        r = self._client.post(f"{self.api_url}/generate", json=body)
        self._check(r)
        logger.info(f"Model '{model}' loaded with keep_alive={keep_alive}")
        return r.json()

    def unload_model(self, model: str) -> dict:
        """
        Force-unload a model from VRAM immediately.

        Uses keep_alive=0 to trigger immediate eviction.
        """
        body = {
            "model": model,
            "prompt": "",
            "keep_alive": 0,
            "stream": False,
        }
        r = self._client.post(f"{self.api_url}/generate", json=body)
        self._check(r)
        logger.info(f"Model '{model}' unloaded from VRAM")
        return r.json()

    def switch_model(
        self,
        from_model: Optional[str],
        to_model: str,
        keep_alive: str = "-1",
    ) -> dict:
        """
        Atomically switch the active model: unload old, load new.

        Args:
            from_model: Model to unload (None to skip unload)
            to_model: Model to load
            keep_alive: How long to keep the new model loaded ("-1" = forever)

        Returns: load response dict
        """
        # Unload the old model
        if from_model and self.model_is_running(from_model):
            logger.info(f"Unloading '{from_model}' to make room for '{to_model}'")
            self.unload_model(from_model)
            # Brief pause for VRAM to be freed
            time.sleep(1.0)

        # Ensure target model is installed
        if not self.model_exists(to_model):
            logger.info(f"Model '{to_model}' not found locally, pulling...")
            self.pull(to_model, stream=False)

        # Load the new model
        return self.load_model(to_model, keep_alive=keep_alive)

    def ensure_model_loaded(self, model: str, keep_alive: str = "-1") -> None:
        """Load a model if it's not already running."""
        if not self.model_is_running(model):
            self.load_model(model, keep_alive=keep_alive)

    # -----------------------------------------------------------------------
    # Inference: Chat
    # -----------------------------------------------------------------------

    def chat(
        self,
        model: str,
        messages: list[dict],
        stream: bool = False,
        think: Optional[Union[bool, str]] = None,
        tools: Optional[list] = None,
        format: Optional[Union[str, dict]] = None,
        options: Optional[dict] = None,
        keep_alive: Optional[str] = None,
    ) -> Union[dict, Generator]:
        """
        Generate a chat response.

        Args:
            model: Model name (e.g. "qwen3.6:27b")
            messages: Chat history as list of {role, content} dicts
            stream: If True, yields partial response dicts
            think: Enable thinking/reasoning (True/False/"high"/"medium"/"low")
            tools: List of tool definitions (JSON schema or Python functions)
            format: "json" or a JSON schema dict for structured outputs
            options: Runtime options (temperature, num_ctx, top_p, etc.)
            keep_alive: Override model keep-alive duration

        Returns: Response dict or generator of partial dicts
        """
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        if think is not None:
            body["think"] = think
        if tools is not None:
            body["tools"] = tools
        if format is not None:
            body["format"] = format
        if options is not None:
            body["options"] = options
        if keep_alive is not None:
            body["keep_alive"] = keep_alive

        if stream:
            return self._stream_request("POST", f"{self.api_url}/chat", body)
        else:
            r = self._client.post(f"{self.api_url}/chat", json=body)
            self._check(r)
            return r.json()

    def chat_simple(self, model: str, prompt: str, system: Optional[str] = None, **kwargs) -> str:
        """
        Simple chat helper: send a single prompt, get back just the text.

        Returns the assistant's content string.
        """
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        result = self.chat(model=model, messages=messages, stream=False, **kwargs)
        return result.get("message", {}).get("content", "")

    # -----------------------------------------------------------------------
    # Inference: Generate (raw completion)
    # -----------------------------------------------------------------------

    def generate(
        self,
        model: str,
        prompt: str,
        stream: bool = False,
        system: Optional[str] = None,
        suffix: Optional[str] = None,
        images: Optional[list[str]] = None,
        think: Optional[Union[bool, str]] = None,
        format: Optional[Union[str, dict]] = None,
        raw: bool = False,
        options: Optional[dict] = None,
        keep_alive: Optional[str] = None,
    ) -> Union[dict, Generator]:
        """
        Generate a raw text completion.

        Args:
            model: Model name
            prompt: Input text
            system: System prompt
            suffix: Fill-in-the-middle suffix
            images: Base64-encoded images
            think: Enable thinking
            format: "json" or JSON schema
            raw: Skip prompt templating
            options: Runtime options
            keep_alive: Override keep-alive

        Returns: Response dict or generator
        """
        body: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
        }
        if system is not None:
            body["system"] = system
        if suffix is not None:
            body["suffix"] = suffix
        if images is not None:
            body["images"] = images
        if think is not None:
            body["think"] = think
        if format is not None:
            body["format"] = format
        if raw:
            body["raw"] = True
        if options is not None:
            body["options"] = options
        if keep_alive is not None:
            body["keep_alive"] = keep_alive

        if stream:
            return self._stream_request("POST", f"{self.api_url}/generate", body)
        else:
            r = self._client.post(f"{self.api_url}/generate", json=body)
            self._check(r)
            return r.json()

    # -----------------------------------------------------------------------
    # Inference: Embeddings
    # -----------------------------------------------------------------------

    def embed(
        self,
        model: str,
        input: Union[str, list[str]],
        truncate: bool = True,
        dimensions: Optional[int] = None,
        options: Optional[dict] = None,
        keep_alive: Optional[str] = None,
    ) -> dict:
        """
        Generate vector embeddings for input text(s).

        Args:
            model: Embedding model name
            input: Text string or list of strings
            truncate: If True, truncate inputs exceeding context window
            dimensions: Number of embedding dimensions
            options: Runtime options
            keep_alive: Override keep-alive

        Returns: Dict with 'embeddings' (list of float lists),
                 'total_duration', 'load_duration', 'prompt_eval_count'
        """
        body: dict[str, Any] = {
            "model": model,
            "input": input,
        }
        if not truncate:
            body["truncate"] = False
        if dimensions is not None:
            body["dimensions"] = dimensions
        if options is not None:
            body["options"] = options
        if keep_alive is not None:
            body["keep_alive"] = keep_alive

        r = self._client.post(f"{self.api_url}/embed", json=body)
        self._check(r)
        return r.json()

    # -----------------------------------------------------------------------
    # OpenAI-Compatible API
    # -----------------------------------------------------------------------

    def openai_chat(
        self,
        model: str,
        messages: list[dict],
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        tools: Optional[list] = None,
        response_format: Optional[dict] = None,
        reasoning_effort: Optional[str] = None,
    ) -> dict:
        """
        Send a chat request via the OpenAI-compatible /v1/chat/completions endpoint.

        This allows using the `openai` Python SDK or any OpenAI-compatible client.
        """
        body: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": stream,
        }
        if temperature is not None:
            body["temperature"] = temperature
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if tools is not None:
            body["tools"] = tools
        if response_format is not None:
            body["response_format"] = response_format
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort

        r = self._client.post(
            f"{self.openai_url}/chat/completions",
            json=body,
            headers={"Authorization": "Bearer ollama"},
        )
        self._check(r)
        return r.json()

    def openai_list_models(self) -> list[dict]:
        """List models via OpenAI-compatible /v1/models endpoint."""
        r = self._mgmt_client.get(
            f"{self.openai_url}/models",
            headers={"Authorization": "Bearer ollama"},
        )
        self._check(r)
        return r.json().get("data", [])

    # -----------------------------------------------------------------------
    # VRAM-Aware Helpers
    # -----------------------------------------------------------------------

    def get_vram_usage(self) -> dict:
        """
        Get VRAM usage from running models.

        Returns: {total_vram_bytes, models: [{name, size_vram, context_length}]}
        """
        running = self.list_running()
        total = sum(m.get("size_vram", 0) for m in running)
        return {
            "total_vram_bytes": total,
            "total_vram_mib": total // (1024 * 1024),
            "models": [
                {
                    "name": m["name"],
                    "size_vram_mib": m.get("size_vram", 0) // (1024 * 1024),
                    "context_length": m.get("context_length", 0),
                }
                for m in running
            ],
        }

    def recommended_context(self, vram_mib: int) -> int:
        """Get the recommended context length for a given VRAM amount."""
        for threshold, ctx in VRAM_CONTEXT_MAP:
            if vram_mib < threshold:
                return ctx
        return 4096

    # -----------------------------------------------------------------------
    # Convenience: Status Summary
    # -----------------------------------------------------------------------

    def status(self) -> dict:
        """
        Return a comprehensive status summary of the Ollama instance.

        Includes: version, installed models, running models, VRAM usage.
        """
        alive = self.is_alive()
        result = {"alive": alive}

        if alive:
            result["version"] = self.version()
            result["installed_models"] = self.list_model_names()
            result["running_models"] = self.list_running_names()
            result["vram"] = self.get_vram_usage()

        return result

    # -----------------------------------------------------------------------
    # Internal Helpers
    # -----------------------------------------------------------------------

    def _check(self, response: httpx.Response):
        """Raise OllamaError if response indicates failure."""
        if response.status_code >= 400:
            try:
                detail = response.json().get("error", response.text)
            except Exception:
                detail = response.text
            raise OllamaError(response.status_code, detail)

    def _stream_request(
        self, method: str, url: str, body: dict, timeout: float = DEFAULT_TIMEOUT
    ) -> Generator[dict, None, None]:
        """Yield line-delimited JSON objects from a streaming response."""
        with httpx.Client(timeout=timeout) as client:
            with client.stream(method, url, json=body) as response:
                if response.status_code >= 400:
                    response.read()
                    try:
                        detail = response.json().get("error", response.text)
                    except Exception:
                        detail = response.text
                    raise OllamaError(response.status_code, detail)

                for line in response.iter_lines():
                    if line.strip():
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            logger.warning(f"Non-JSON line in stream: {line}")


# ---------------------------------------------------------------------------
# CLI Quick-Test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)
    oc = OllamaController()

    if not oc.is_alive():
        print("❌ Ollama server is not running. Start it with: ollama serve")
        sys.exit(1)

    print("=" * 60)
    print("AXiomEngine OllamaController — System Status")
    print("=" * 60)

    status = oc.status()
    print(f"  Version:  {status['version']}")
    print(f"  Installed: {', '.join(status['installed_models']) or 'none'}")
    print(f"  Running:   {', '.join(status['running_models']) or 'none'}")
    vram = status["vram"]
    print(f"  VRAM Used: {vram['total_vram_mib']} MiB across {len(vram['models'])} model(s)")
    for m in vram["models"]:
        print(f"    • {m['name']}: {m['size_vram_mib']} MiB, ctx={m['context_length']}")
    print("=" * 60)

    # Quick inference test if any model is available
    models = status["installed_models"]
    if models:
        test_model = models[0]
        print(f"\n🧪 Quick inference test with '{test_model}'...")
        try:
            answer = oc.chat_simple(test_model, "Say 'AXiomEngine ready' in exactly two words.")
            print(f"  Response: {answer[:100]}")
            print("  ✅ Inference OK")
        except Exception as e:
            print(f"  ❌ Inference failed: {e}")
    else:
        print("\n⚠️  No models installed. Pull one with: ollama pull qwen3.6:27b")

    oc.close()

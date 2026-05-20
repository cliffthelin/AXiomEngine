#!/usr/bin/env python3
import json
import httpx
import asyncio
import os
import time
from typing import List, Dict, Optional, Any, AsyncGenerator, Literal, Union
from pydantic import BaseModel, Field
from pathlib import Path
from scripts.pi_config import get_agent_dir

# --- Types ---

class ModelCost(BaseModel):
    input: float = 0.0
    output: float = 0.0
    cache_read: float = 0.0
    cache_write: float = 0.0

class OpenAICompletionsCompat(BaseModel):
    supportsStore: bool = True
    supportsDeveloperRole: bool = True
    supportsReasoningEffort: bool = True
    supportsUsageInStreaming: bool = True
    supportsStrictMode: bool = True
    maxTokensField: Literal["max_completion_tokens", "max_tokens"] = "max_completion_tokens"
    thinkingFormat: Literal["openai", "deepseek", "zai", "qwen"] = "openai"

class Model(BaseModel):
    id: str
    name: str
    api: str
    provider: str
    cost: ModelCost = Field(default_factory=ModelCost)
    context_window: int = 128000
    max_tokens: int = 4096
    base_url: Optional[str] = None
    reasoning: bool = False
    input: List[str] = ["text"]
    compat: Optional[OpenAICompletionsCompat] = None

class AIEvent(BaseModel):
    type: str
    delta: Optional[str] = None
    content: Optional[Any] = None
    reason: Optional[str] = None
    thinking: Optional[str] = None

# --- Registry ---

class AIRegistry:
    def __init__(self):
        ollama_compat = OpenAICompletionsCompat(
            supportsStore=False,
            supportsDeveloperRole=False,
            supportsReasoningEffort=False,
            supportsUsageInStreaming=False,
            supportsStrictMode=False,
            maxTokensField="max_tokens",
            thinkingFormat="qwen",
        )
        self.models: Dict[str, Model] = {
            "ollama/qwen3.6:27b": Model(
                id="qwen3.6:27b", name="Qwen 3.6 27B (Ollama/P40)", api="openai-completions", provider="ollama",
                base_url="http://127.0.0.1:11437/v1", context_window=32768, max_tokens=4096, reasoning=True,
                compat=ollama_compat
            ),
            "ollama/gemma4:e2b": Model(
                id="gemma4:e2b", name="Gemma4 E2B Researcher (Ollama/RTX 3070)", api="openai-completions", provider="ollama",
                base_url="http://127.0.0.1:11436/v1", context_window=32768, max_tokens=2048,
                compat=ollama_compat
            ),
            "ollama/cmdmbox/skill-expert": Model(
                id="cmdmbox/skill-expert", name="Skill Expert (Ollama/RTX 3070)", api="openai-completions", provider="ollama",
                base_url="http://127.0.0.1:11436/v1", context_window=32768, max_tokens=2048,
                compat=ollama_compat
            ),
            "ollama/qwen3.6:35b": Model(
                id="qwen3.6:35b", name="Qwen 3.6 35B (Ollama fallback)", api="openai-completions", provider="ollama",
                base_url="http://127.0.0.1:11434/v1", context_window=32768, max_tokens=4096, reasoning=True,
                compat=ollama_compat
            ),
            "openai/gpt-4o": Model(
                id="gpt-4o", name="GPT-4o", api="openai-completions", provider="openai",
                cost=ModelCost(input=5.0, output=15.0), context_window=128000, input=["text", "image"]
            ),
            "anthropic/claude-3-5-sonnet": Model(
                id="claude-3-5-sonnet-20241022", name="Claude 3.5 Sonnet", api="anthropic-messages", provider="anthropic",
                cost=ModelCost(input=3.0, output=15.0), context_window=200000, reasoning=True, input=["text", "image"]
            ),
            "deepseek/deepseek-reasoner": Model(
                id="deepseek-reasoner", name="DeepSeek R1", api="openai-completions", provider="deepseek",
                base_url="https://api.deepseek.com/v1", cost=ModelCost(input=0.14, output=0.28),
                context_window=64000, reasoning=True,
                compat=OpenAICompletionsCompat(thinkingFormat="deepseek", supportsDeveloperRole=False)
            )
        }
        self.load_custom_models()

    def load_custom_models(self):
        config_paths = [
            get_agent_dir() / "models.json",
            Path.cwd() / ".pi" / "models.json",
        ]
        for config_path in config_paths:
            if not config_path.exists():
                continue
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    providers = config.get("providers", {})
                    for p_name, p_config in providers.items():
                        self.register_provider(p_name, p_config)
            except Exception as e:
                print(f"Failed to load custom models from {config_path}: {e}")

    def get_model(self, id: str) -> Optional[Model]:
        model = self.models.get(id)
        if model:
            return model
        # Convenience aliases keep local Ollama usable from short model names.
        aliases = {
            "qwen3.6": "ollama/qwen3.6:27b",
            "qwen3.6:27b": "ollama/qwen3.6:27b",
            "gemma4:e2b": "ollama/gemma4:e2b",
            "cmdmbox/skill-expert": "ollama/cmdmbox/skill-expert",
        }
        alias = aliases.get(id)
        return self.models.get(alias) if alias else None

    def register_provider(self, provider_name: str, config: Dict[str, Any]):
        base_url = config.get("baseUrl")
        api_key = config.get("apiKey")
        provider_compat = config.get("compat")
        
        if "models" in config:
            for m_data in config["models"]:
                m_id = f"{provider_name}/{m_data['id']}"
                # Merge compat settings
                m_compat = m_data.get("compat") or provider_compat
                compat_obj = OpenAICompletionsCompat(**m_compat) if m_compat else None
                
                self.models[m_id] = Model(
                    id=m_data["id"],
                    name=m_data.get("name", m_data["id"]),
                    api=config.get("api", "openai-completions"),
                    provider=provider_name,
                    cost=ModelCost(**m_data.get("cost", {"input": 0.0, "output": 0.0})),
                    context_window=m_data.get("contextWindow", 128000),
                    base_url=base_url,
                    reasoning=m_data.get("reasoning", False),
                    compat=compat_obj
                )
        if api_key:
            os.environ[f"{provider_name.upper()}_API_KEY"] = api_key

registry = AIRegistry()

# --- Main API ---
# (stream, complete, _transform_context, _stream_openai, _stream_anthropic implementations...)
async def stream(model_id: str, context: Dict[str, Any], options: Dict[str, Any] = None) -> AsyncGenerator[AIEvent, None]:
    model = registry.get_model(model_id)
    if not model:
        yield AIEvent(type="error", content=f"Model {model_id} not found")
        return
    options = options or {}
    transformed_context = _transform_context(context, model)
    if model.api == "openai-completions":
        async for event in _stream_openai(model, transformed_context, options): yield event
    elif model.api == "anthropic-messages":
        async for event in _stream_anthropic(model, transformed_context, options): yield event
    else:
        yield AIEvent(type="error", content=f"API {model.api} not implemented")

async def complete(model_id: str, context: Dict[str, Any], options: Dict[str, Any] = None) -> Dict[str, Any]:
    full_content = ""
    full_thinking = ""
    last_reason = "stop"
    async for event in stream(model_id, context, options):
        if event.type == "text_delta": full_content += event.delta
        elif event.type == "thinking_delta": full_thinking += event.delta
        elif event.type == "done": last_reason = event.reason
    return {"role": "assistant", "content": full_content, "metadata": {"thinking": full_thinking, "stop_reason": last_reason}}

def _transform_context(context: Dict[str, Any], target_model: Model) -> Dict[str, Any]:
    messages = []
    for m in context.get("messages", []):
        msg = m.copy()
        if not target_model.reasoning and "thinking" in m.get("metadata", {}):
            msg["content"] = f"<thinking>\n{m['metadata']['thinking']}\n</thinking>\n{m['content']}"
        messages.append(msg)
    return {**context, "messages": messages}

async def _stream_openai(model: Model, context: Dict[str, Any], options: Dict[str, Any]) -> AsyncGenerator[AIEvent, None]:
    base_url = model.base_url or "https://api.openai.com/v1"
    if not base_url.endswith("/chat/completions"): base_url += "/chat/completions"
    
    from scripts.auth_manager import get_auth_manager
    auth = get_auth_manager()
    api_key = options.get("apiKey") or auth.get_api_key(model.provider)
    
    headers = {"Authorization": f"Bearer {api_key or 'ollama'}"}
    payload = {
        "model": model.id,
        "messages": [{"role": m["role"], "content": m["content"]} for m in context["messages"]],
        "stream": True,
        "temperature": options.get("temperature", 0.7),
        model.compat.maxTokensField if model.compat else "max_completion_tokens": options.get("max_tokens", model.max_tokens),
    }
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", base_url, json=payload, headers=headers, timeout=60) as response:
                yield AIEvent(type="start")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]; 
                        if data_str == "[DONE]": break
                        data = json.loads(data_str)
                        choice = data["choices"][0]; delta = choice.get("delta", {})
                        if "content" in delta and delta["content"]: yield AIEvent(type="text_delta", delta=delta["content"])
                        if "reasoning_content" in delta: yield AIEvent(type="thinking_delta", delta=delta["reasoning_content"])
                        if "reasoning" in delta: yield AIEvent(type="thinking_delta", delta=delta["reasoning"])
                yield AIEvent(type="done", reason="stop")
    except Exception as e: yield AIEvent(type="error", content=str(e))

async def _stream_anthropic(model: Model, context: Dict[str, Any], options: Dict[str, Any]) -> AsyncGenerator[AIEvent, None]:
    from scripts.auth_manager import get_auth_manager
    auth = get_auth_manager()
    api_key = options.get("apiKey") or auth.get_api_key("anthropic")
    
    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    messages = [{"role": m["role"], "content": m["content"]} for m in context["messages"] if m["role"] != "system"]
    system = context.get("systemPrompt", "") or next((m["content"] for m in context["messages"] if m["role"] == "system"), "")
    payload = {"model": model.id, "messages": messages, "system": system, "max_tokens": model.max_tokens, "stream": True}
    if model.reasoning and options.get("thinking"):
        payload["thinking"] = {"type": "enabled", "budget_tokens": options.get("thinkingTokens", 2048)}
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", "https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=60) as response:
                yield AIEvent(type="start")
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:]); type = data.get("type")
                        if type == "content_block_delta":
                            delta = data["delta"]
                            if delta["type"] == "text_delta": yield AIEvent(type="text_delta", delta=delta["text"])
                            if delta["type"] == "thinking_delta": yield AIEvent(type="thinking_delta", delta=delta["thinking"])
                yield AIEvent(type="done", reason="stop")
    except Exception as e: yield AIEvent(type="error", content=str(e))

from scripts.pi_ai import registry
from scripts.auth_manager import AuthManager
from scripts.agent_types import AgentState


def test_builtin_ollama_models_registered():
    qwen = registry.get_model("ollama/qwen3.6:27b")
    researcher = registry.get_model("ollama/gemma4:e2b")
    skill = registry.get_model("ollama/cmdmbox/skill-expert")

    assert qwen is not None
    assert qwen.base_url == "http://127.0.0.1:11437/v1"
    assert researcher is not None
    assert researcher.base_url == "http://127.0.0.1:11436/v1"
    assert skill is not None
    assert skill.base_url == "http://127.0.0.1:11436/v1"


def test_ollama_short_aliases_resolve():
    assert registry.get_model("qwen3.6").id == "qwen3.6:27b"
    assert registry.get_model("gemma4:e2b").provider == "ollama"
    assert registry.get_model("cmdmbox/skill-expert").provider == "ollama"


def test_ollama_auth_is_local_dummy_key():
    assert AuthManager().get_api_key("ollama") == "ollama"


def test_agent_state_defaults_to_local_ollama():
    assert AgentState().model == "ollama/qwen3.6:27b"
